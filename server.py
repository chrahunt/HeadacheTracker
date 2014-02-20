from flask import Flask, render_template
app = Flask(__name__)

@app.route("/sample")
def sample():
	return render_template("sample.html")

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=3000)
