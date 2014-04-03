from flask import Flask, session, request, escape, redirect, url_for, render_template, Response
import MySQLdb 
import csv
import StringIO

from utils import db_connect, get_salt, phash
from forms.user_forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.secret_key = 'DS_34*^DS3*90!_ji*217*#NV'

@app.route("/")
def index():
	if 'logged' in session:
		return redirect(url_for('homepage'))
	form = RegistrationForm()
	return render_template("index.html", selectedNav='Home', form=form)

# TODO: Need to create a separate logout route/method.
@app.route("/login", methods=['GET','POST'])
def login(): 
	form = LoginForm(request.form)

	# In case some authenticated user navigates to this page.
	if 'logged' in session:
		session.pop('logged', None)
	
	if request.method == 'POST' and form.validate():
		session['logged'] = form.username.data
		return redirect(url_for('homepage'))

	return render_template("login.html", selectedNav='Login', form=form)

@app.route("/logout")
def logout():
	if 'logged' in session:
		session.pop('logged', None)
	
	return redirect(url_for('index'))

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

@app.route("/add_entry", methods=['GET', 'POST'])
def addEntry():
	db = db_connect()
	cur = db.cursor()

	if request.method == "POST":
		start_datetime = request.form['startd'] + " " + request.form['startt']
		end_datetime = request.form['endd'] + " " + request.form['endt']
		query = "SELECT id FROM users WHERE username='" + session['logged'] + "'"
		cur.execute(query)
		user_id = cur.fetchone()
		print user_id		
		
		query = "INSERT INTO headache_entries (entry_start, entry_end, severity, user_id) VALUES ('" + start_datetime + "', '" + end_datetime + "', '" + request.form['severity'] + "', '" + str(user_id[0]) + "')"
		print query
		cur.execute(query)
		db.commit()
		
	return redirect(url_for('homepage'))

@app.route("/homepage", methods=['GET','POST'])
def homepage():
	db = db_connect()
	cur = db.cursor(MySQLdb.cursors.DictCursor)
	
	if request.method == 'POST':
		session['logged'] = request.form['username']
		
	query = "SELECT username, first_name AS firstname, last_name AS lastname FROM users WHERE username='" + session['logged'] + "'"
	print query
	cur.execute(query)
	
	userInfo = cur.fetchone()
	
	allInfo = userInfo

	query = "SELECT DATE(entry_start) AS start_date, TIME(entry_start) AS start_time, DATE(entry_end) AS end_date, TIME(entry_end) AS end_time, severity FROM headache_entries WHERE user_id = (SELECT id FROM users WHERE username='" + session['logged'] + "') ORDER BY entry_start DESC"
	print query
	cur.execute(query)

	entries = cur.fetchall()
	print entries[0]
	
	return render_template("homepage.html", selectedNav='Home', allInfo=allInfo, entries=entries, loggedIn=True)

@app.route("/export", methods=['GET', 'POST'])
def export():
	# Request for export data.
	if request.method == 'POST':
		db = db_connect()
		cur = db.cursor(MySQLdb.cursors.DictCursor);
		query = "SELECT DATE(h.entry_start) AS start_date, TIME(h.entry_start) AS start_time, DATE(h.entry_end) AS end_date, TIME(h.entry_end) AS end_time, h.severity FROM headache_entries h JOIN users u ON h.user_id = u.id WHERE u.l_username = LOWER('{}')".format(session['logged'])
		cur.execute(query)
		# Get all entries at once.
		entries = cur.fetchall();

		# Save results parsed as csv to file in-memory.
		string_buffer = StringIO.StringIO()
		w = csv.DictWriter(string_buffer, entries[0].keys())
		w.writeheader()
		w.writerows(entries)
		csv_content = string_buffer.getvalue()
		string_buffer.close()

		# Response with export data.
		return Response(csv_content,
				mimetype="text/csv",
				headers={
					"Content-Disposition": "attachment;filename=export.csv"
					})

	return render_template("export.html")

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
	
