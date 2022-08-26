# Client
_400 = [400, "Bad Request"]
_401 = [401, "Unauthorized"]
_403 = [403, "Forbidden"]
_404 = [404, "Page Not Found"]
_405 = [405, "Method Not Allowed"]
_406 = [406, "Not Acceptable"]
_408 = [408, "Request Timed Out"]
_409 = [409, "Conflict"]
_410 = [410, "Gone"]
_413 = [413, "Payload To Large"]

# Server
_500 = [500, "Internal Server Error"]
_501 = [501, "Not Implemented"]
_502 = [502, "Bad Gateway"]
_503 = [503, "Service Unavailable"]
_504 = [504, "Gateway Timeout"]
_505 = [505, "HTTP Version Not Supported"]

# Errors
errors = [
	_400, _401, _403, _404, _405, 
	_406, _408, _409, _410, _413,
	_500, _501, _502, _503, _504,
	_505
]

def init(app, flask):
	for error in errors:
		no, msg = error
		exec(f"""
@app.errorhandler({no})
def _{no}_handler(e):
	return flask.render_template('error.html', no={no}, msg='{msg}'), {no}
	  	""", locals(), locals())