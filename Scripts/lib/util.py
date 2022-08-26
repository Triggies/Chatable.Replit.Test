from datetime import date as _date, datetime as _datetime
import pytz
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

def uid(i): return os.urandom(i).hex()
def date(): return str(_date.today())
def time(): return str(_datetime.now(pytz.timezone("US/Central")).strftime("%H:%M:%S"))
def datetime(): return f"{date()}/{time()}"
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