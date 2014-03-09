from flask import Flask, session, request, escape, redirect, url_for, render_template
import MySQLdb 

from utils import db_connect, get_salt, phash
from forms.user_forms import RegistrationForm

app = Flask(__name__)

app.secret_key = 'DS_34*^DS3*90!_ji*217*#NV'

@app.route("/")
def index():
	if 'logged' in session:
		return redirect(url_for('homepage'))
	form = RegistrationForm()
	return render_template("index.html", selectedNav='Home', loggedIn='false', form=form)

# TODO: Need to create a separate logout route/method.
@app.route("/login", methods=['GET','POST'])
def login(): 
	if 'logged' in session:
		session.pop('logged', None)
		return redirect(url_for('index'))
	return render_template("login.html", selectedNav='Login')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		db = db_connect()
		cur = db.cursor()
		salt = get_salt()
		password_hash = phash(form.password.data + salt)
		# TODO: Clean up this handling.
		# Handles case where email is not present, inserts NULL below.
		# Notice lack of single quotes in query which facilitates this.
		if form.email.data != "":
			email = "'{}'".format(form.email.data)
		else:
			email = "NULL"

		query = "INSERT INTO users (username, l_username, password_hash, salt, email) " \
				"VALUES ('{username}', LOWER('{username}'), '{password_hash}', " \
				"'{salt}', {email})".format(
						username=form.username.data,
						password_hash=password_hash,
						salt=salt,
						email=email
					)
		cur.execute(query)
		db.commit()

		session['logged'] = form.username.data
		return redirect(url_for('homepage'))
	
	return render_template("register.html", selectedNav='Register', form=form)

@app.route("/homepage", methods=['GET','POST'])
def homepage():
	db = db_connect()
	cur = db.cursor()
	
	if request.method == 'POST':
		session['logged'] = request.form['username']
		
	query = "SELECT * FROM users WHERE username='" + session['logged'] + "'"
	print query
	cur.execute(query)
	
	userInfo = cur.fetchone()
	
	allInfo = {
		'username' : userInfo[1],
		'password' : userInfo[2],
		'firstname' : userInfo[3],
		'lastname' : userInfo[4]
	}
		
	return render_template("homepage.html", selectedNav='Home', allInfo=allInfo, loggedIn='true')

@app.route("/dbsample")
def dbsample():
	db = db_connect()
	cur = db.cursor()
	# Example using DictCursor, which returns rows as Dicts, rather than Tuples
	cur2 = db.cursor(MySQLdb.cursors.DictCursor)

	query = "SELECT * FROM users"
	cur.execute(query)
	cur2.execute(query)

	users = cur.fetchall()
	users2 = cur2.fetchall()
	print(users)
	print(users2)
	return render_template("dbsample.html", users=users, users2=users2)

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=3000)
	
