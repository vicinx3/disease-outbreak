from flask import Flask, request
from PHASE_1.API_SourceCode.server.apis import blueprint as api 
from logging import FileHandler, INFO
from datetime import datetime

file_handler = FileHandler('Error.log')
file_handler.setLevel(INFO)

app = Flask(__name__)
prev_time = datetime.now()
@app.before_request
def log_info():
	app.logger.info('Original query data : %s', request.headers)
	app.logger.info('Original query data : %s', request.get_data())

@app.after_request
def log_response(response):
	now = datetime.now()
	op_time = now - prev_time
	app.logger.info('Query took ' + str(op_time.microseconds/1000) + ' milliseconds')
	app.logger.info('Response sent: %s', response.status_code)
	app.logger.info('Response sent: %s', response.get_json())
	return response

app.logger.addHandler(file_handler)
app.register_blueprint(api)
app.config['RESTPLUS_MASK_SWAGGER'] = False # Removes x-fields parameters 