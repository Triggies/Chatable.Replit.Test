import database
import flask
import l_utils as utils

app = flask.Flask(__name__)

@app.route("/account")
def account():
	return flask.render_template("account.html")
	

@app.route("/accounts/log-in/", methods=["POST"])
def run_login():
	username = flask.request.form.get("username")
	password = flask.request.form.get("password")

	status, err = database.login({
		"username": username, 
		"password": password
	})

	if status:
		return flask.redirect("/account")

	return flask.render_template("login.html", error_text=utils.handle_error(err))

@app.route("/log-in")
def log_in_page():
	return flask.render_template("login.html")


@app.route("/accounts/sign-up/", methods=["POST"])
def run_sign_up():
	username = flask.request.form.get("username")
	password = flask.request.form.get("password")

	status, err = database.signup({
		"username": username, 
		"password": password
	})

	if status:
		return flask.redirect("/account")

	return flask.render_template("signup.html", error=utils.handle_error(err))

@app.route("/sign-up")
def sign_up_page():
	return flask.render_template("signup.html")


@app.route("/")
def main():
	print(utils.view_database())
	database.init()
	return flask.render_template("home.html")

if __name__ == "__main__":
	app.run("0.0.0.0")