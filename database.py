from replit import db
from l_utils import *
import hashlib
import string
import os


def init():
	if not "users" in db: db["users"] = {}
	if not "messages" in db: db["messages"] = {}

def __salt():
	return os.urandom(50).hex()

def encrypt(string, salt):
	string = f"{salt}{string}{pepper}".encode()
	return hashlib.sha3_512(string).hexdigest()

def create_cookie():
	return os.urandom(20).hex()


def save_message(auth, message, msg_id):
	status, error = validate_auth(auth)
	if not status:
		return [status, error]
	
	db['messages'][auth['username']][msg_id] = {
		'msg': message,
		'edited': False
	}
	
	return success

def edit_message(auth, new_message, msg_id):
	status, error = validate_auth(auth)
	if not status:
		return [status, error]

	db['messages'][auth['username']][msg_id] = {
		'msg': new_message,
		'edited': True
	}
	
	return success

def delete_message(auth, msg_id):
	status, error = validate_auth(auth)
	if not status:
		return [status, error]

	del db['messages'][auth['username']][msg_id]

	return success


def legal_username(username: str):
	if len(username) > 15: return error(UTL)
	
	legal_characters = [c for c in string.ascii_letters]
	legal_characters.append("_")
	for c in username:
		if not c in legal_characters: return error(IUNC)
	return success

def signup(credentials):
	username, password = credentials['username'], credentials['password']

	status, err = legal_username(username)
	if not status: return error(err)
	if username in db['users']: return error(UAE)
	if not len(password) > 5: return error(PTS)

	salt = __salt()
	password = encrypt(password, salt)
	db['users'][username] = {
		'password': f"{salt}.{password}",
		'cookie': create_cookie()
	}
	db['messages'][username] = {}
	
	return success

def __validate_password(username, password):
	salt, encrypted_password = db["users"][username]["password"].split(".")

	return encrypt(password, salt) == encrypted_password

def login(credentials):
	username, password = credentials["username"], credentials["password"]

	if not __user_exists(username): return [False, UDNE]
	if not __validate_password(username, password):
		return error(IUP)
	
	db["users"][username]["cookie"] = create_cookie()
	return success

def signout():
	pass

def delete_account(username, password):
	if not __validate_password(username, password):
		return [False, IUP]

	del db["users"][username]
	del db["messages"][username]
	
	return success
	

def __user_exists(username: str) -> bool:
	return username in db['users']

def validate_auth(auth: dict) -> list:
	username, cookie = auth['username'], auth['cookie']
	
	if not __user_exists(username): 
		return [False, UDNE]

	if not db['users'][username]['cookie'] == cookie:
		return [False, IUC]

	return success