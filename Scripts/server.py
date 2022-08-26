from Scripts.lib import errors, util
from Scripts.db import database
import flask

app = flask.Flask(__name__, template_folder="../templates")

###############################################################
errors.init(app, flask)
###############################################################

@app.route("/accounts/log-in/", methods=["POST"])
def login():
	username = flask.request.form.get("username")
	password = flask.request.form.get("password")

	status, err = database.login({
		"username": username, 
		"password": password
	})

	if status:
		return flask.render_template("account/redirect.html", cookie=database.get_cookie(username))

	return flask.render_template("account/login.html", error_text=util.handle_error(err))

@app.route("/log-in")
def login_page():
	return flask.render_template("account/login.html")

###############################################################

@app.route("/accounts/sign-up/", methods=["POST"])
def signup():
	username = flask.request.form.get("username")
	password = flask.request.form.get("password")

	status, err = database.signup({
		"username": username, 
		"password": password
	})

	if status:
		return flask.render_template("account/redirect.html", cookie=database.get_cookie(username))

	return flask.render_template("account/signup.html", error=util.handle_error(err))

###############################################################

@app.route("/account")
def account():
	return flask.render_template("account/account.html")

###############################################################

@app.route("/sign-up")
def signup_page():
	return flask.render_template("account/signup.html")

###############################################################

@app.route("/")
def main():
	database.init()
	return flask.render_template("home.html")

###############################################################

def init():
	app.run("0.0.0.0")