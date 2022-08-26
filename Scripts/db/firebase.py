from firebase_admin import db
import firebase_admin as admin

USERS = "users/"
COOKIES = "cke"
PASSWORD = "pwd"
MESSAGES = "msg"

def init():
	try: 
		credentials = admin.credentials.Certificate("credentials.json")
		admin.initialize_app(credentials, {
			"databaseURL": "https://chatical-fa078-default-rtdb.firebaseio.com"
		})
	except ValueError:
		return

def ref(reference):
	return db.reference(reference)

def child(child):
	return db.reference(USERS).child(child)

def save(reference: str, child: str, data: dict):
	ref = db.reference(reference)
	ref.child(child).set(data)

def update(child: ref, key, value):
	child.update({key: value})

def delete(node):
	node.delete()

def read(db_reference):
	data = db.reference(db_reference).get()
	return {True: [], False: data}[data == None]