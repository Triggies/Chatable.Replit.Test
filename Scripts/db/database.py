from Scripts.db.firebase import USERS, COOKIES, PASSWORD, MESSAGES, ref, child
from Scripts.db import firebase
from Scripts.lib import util
import hashlib
import string
import os
	
init = firebase.init

###############################################################

def get_cookie(username):
	return firebase.read(f"users/{username}/cke")

###############################################################
########################### MESSAGE ###########################
###############################################################

def save_message(auth, message):
	status, error = validate_auth(auth)
	if not status:
		return [status, error]
	
	firebase.save(USERS, f"{auth['username']}/msg", {
		id(24): {
			"content": message,
			"editied": False,
			"datetime": datetime()
		}
	})
	
	return success

###############################################################

def edit_message(auth, new_message, msg_id):
	status, error = validate_auth(auth)
	if not status:
		return [status, error]

	firebase.update(child(f"{auth['username']}/msg"), msg_id, {
		"content": new_message,		
		"edited": True
	})
	
	return success

###############################################################

def delete_message(auth, msg_id):
	status, error = validate_auth(auth)
	if not status:
		return [status, error]

	firebase.delete(f"{auth['username']}/msg/{msg_id}")

	return success

###############################################################
########################### ACCOUNT ###########################
###############################################################

def legal_username(username: str):
	if len(username) > 15: return error(UTL)
	
	legal_characters = [c for c in string.ascii_letters]
	legal_characters.append("_")
	for c in username:
		if not c in legal_characters: return error(IUNC)
	return success

###############################################################

def signup(credentials):
	username, password = credentials['username'], credentials['password']
	users = list(firebase.read("users"))

	status, err = legal_username(username)
	if not status: return error(err)
	if username in users: return error(UAE)
	if not len(password) > 5: return error(PTS)

	salt = uid(50)
	password = encrypt(password, salt)
	firebase.save(USERS, username, {
		PASSWORD: f"{salt}.{password}",
		COOKIES: uid(20),
		MESSAGES: {}
	})
	
	return success

###############################################################

def __validate_password(username, password):
	salt, encrypted_password = firebase.read(f"users/{username}/pwd").split(".")

	return encrypt(password, salt) == encrypted_password

###############################################################

def login(credentials):
	username, password = credentials["username"], credentials["password"]

	if not __user_exists(username): return error(UDNE)
	if not __validate_password(username, password):
		return error(IUP)
	
	firebase.update(child(username), "cke", uid(20))
	return success

###############################################################

def signout():
	pass

###############################################################

def delete_account(username, password):
	if not __validate_password(username, password):
		return error(IUP)
	
	firebase.delete(child(username))
	
	return success
	
###############################################################
############################ EXTRA ############################
###############################################################

def encrypt(string, salt):
	string = f"{salt}{string}{pepper}".encode()
	return hashlib.sha3_512(string).hexdigest()

###############################################################

def __user_exists(username: str) -> bool:
	users = firebase.read("users")
	return {True: username in users, False: False}[not users is None]

###############################################################

def validate_auth(auth: dict) -> list:
	username, cookie = auth['username'], auth['cookie']
	
	if not __user_exists(username): 
		return error(UDNE)

	if not get_cookie(username):
		return error(IUC)

	return success