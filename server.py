from flask import Flask, session, request, escape, redirect, url_for, render_template
import MySQLdb 
import random
import hashlib

from utils import db_connect

app = Flask(__name__)

app.secret_key = 'DS_34*^DS3*90!_ji*217*#NV'

@app.route("/")
def index():
	if 'logged' in session:
		return redirect(url_for('homepage'))
	return render_template("index.html", selectedNav='Home', loggedIn='false')

@app.route("/login", methods=['GET','POST'])
def login(): 
	if 'logged' in session:
		session.pop('logged', None)
		return redirect(url_for('index'))
	return render_template("login.html", selectedNav='Login')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		return registration_controller(request)
	
	return render_template("register.html", selectedNav='Register')

def registration_controller(request):
	username = request.form['username']
	password1 = request.form['password1']
	password2 = request.form['password2']
	password = ""
	email = request.form['email']
	errors = []
	error = False
	db = db_connect()
	cur = db.cursor()

	# Check that passwords match
	if password1 != password2:
		errors.append("The passwords don't match!")
		error = True
	else:
		password = password1
		# Check that password meets length requirements
		if password.length() < 6:
			errors.append("That password is too short (minimum of 6 characters.")
			error = True

		# TODO: Check that password meets complexity requirements
		
	# Check that username is not taken
	# TODO: String escape
	query = "SELECT COUNT(*) FROM users WHERE l_username=LOWER('" + username + "')"
	cur.execute(query)

	userInfo = cur.fetchone()
	print userInfo

	# If there is an error, redirect back to the page and pass in the error messages

	# Otherwise, generate a salt, hash the password, store everything in the
	# database, set the logged session variable

	# Add the email address to the user. Should this 
	if error:
		return render_template("register.html", selectedNav='Register', errors=errors)
	else:
		# Set logged in user
		return render_template("homepage.html", selectedNav='Home')

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
	
