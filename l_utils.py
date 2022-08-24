from replit import db
import os

UDNE = "USER_DOES_NOT_EXIST"
IUC = "INVALID_USER_COOKIE"
UAE = "USERNAME_ALREADY_EXISTS"
IUP = "INVALID_USER_PASSWORD"
IUNC = "INVALID_USERNAME_CHARACTER"
UTL = "USERNAME_TO_LONG"
PTL = "PASSWORD_TO_LONG"
PTS = "PASSWORD_TO_SHORT"

pepper = os.getenv("PEPPER")
success = [True, None]
def error(n): return [False, n]

def handle_error(err):
	return {
		UDNE: "Account does not exist.",
		UAE: "Username already exists.",
		IUP: "Incorrect Username or Password.",
		IUNC: "Usernames may only contain alphabet letters or _",
		UTL: "Username length is to large. (Max: 14)",
		PTL: "Password length is to large. (Max: 20)",
		PTS: "Password length is to short. (Min: 6)"
	}[err]
	
# DEVELOPMENT
def view_database():
	db_users = db["users"]
	users = [user for user in db_users.keys()]
	#cookies = [db_users[user]["cookie"] for user in users]
	#passwords = [db_users[user]["password"] for user in users]
	template = """[
	'{username}': [
		'password': '{password}',
		'cookie': '{cookie}'
	]
],\n"""
	f = ""
	for user in users:
		password = db_users[user]["password"]
		cookie = db_users[user]["cookie"]

		f += template.format(username=user, password=password, cookie=cookie)
	return f#[users, cookies, passwords]