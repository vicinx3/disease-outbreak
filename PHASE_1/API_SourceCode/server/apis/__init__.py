from flask import Blueprint 
from flask_restplus import Api 

from .who import api as who
from .jhu import api as jhu

blueprint = Blueprint('api', __name__)
api = Api(blueprint, 
	title='Codeonavirus D.O.T.',
	version='1.0',
	description='WHO knows where the disease outbreaks are? We do! The Codeonavirus D.O.T. (Disease Outbreak Tracker) is a RESTful API for WHO disease outbreaks that returns news articles of breakouts, as well as daily reports of the COVID-19 situation provided by John Hopkins University.'  
)

api.add_namespace(who)
api.add_namespace(jhu)