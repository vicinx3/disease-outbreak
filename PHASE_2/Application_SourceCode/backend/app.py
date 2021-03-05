import time
from flask import Flask, make_response
from main_page import main_page
from prediction_page import prediction_page 
from covid_page import covid_page

app = Flask(__name__)

app.register_blueprint(main_page, url_prefix='/main')
app.register_blueprint(prediction_page, url_prefix='/prediction')
app.register_blueprint(covid_page, url_prefix='/covid')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
  response.headers.add('Access-Control-Allow-Methods', 'GET')
  return response