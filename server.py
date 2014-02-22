from flask import Flask, render_template
from utils import db_connect
app = Flask(__name__)

@app.route("/sample")
def sample():
	return render_template("sample.html")

@app.route("/dbsample")
def dbsample():
	db = db_connect()
	cur = db.cursor()
	query = "SELECT * FROM users"
	cur.execute(query)
	users = cur.fetchall()
	return render_template("dbsample.html", users=users)

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=3000)
