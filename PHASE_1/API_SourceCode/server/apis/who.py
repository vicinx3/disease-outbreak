from flask import request 
from flask_restplus import Namespace, Resource, fields, abort 
from datetime import datetime
import logging
import json
import re
from .sample.who_response import sample_who_response
from PHASE_1.API_SourceCode.database.db import db_query
from .models import error

logging.basicConfig(filename='Error.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
api = Namespace('WHO', description='World Health Organisation', path='/who')

# Models 
error = api.model('Error', model=error.model)

query = api.model('WHO Query', {
	'start_date': fields.Date(required=True, description='Required.\nStart date of period of publication, inclusive.\nMust be in YYYY-MM-DD format and precede end_date.', example="2005-08-26"),
	'end_date': fields.Date(required=True, description='Required.\nEnd date of period of publication, inclusive.\nMust be in YYYY-MM-DD format and succeed start_date.', example="2005-09-23"),
	'key_terms': fields.String(description='Key terms are comma separated and case-insensitive.\nArticles that include at least one key term will be included in the response.\nIf field is absent, key terms are not considered.', example="Yellow fever"),
	'location': fields.String(description='Filter location by comma-separated case-insensitive string: continent,country,state,city\nArticles that have at least one report with at least one location which matches the provided location query will be included in the response.\nEmpty fields will match any.\n', example="Africa,,,", default=",,,")
})

location = api.model('WHO Location', {
	'continent': fields.String(description='Large expanses of land, specifically Antarctica, Africa, Asia, Europe, Oceania, North America and South America.', example='Africa'),
	'country': fields.String(description='Country or soverign state territory.\nRequires existence of continent.', example='Burkina Faso'),
	'state': fields.String(description='Subnational division.\nIncludes states, provinces, prefectures, regions and districts.\nRequires existence of continent and country.', example='Noumbiel Province'),
	'city': fields.String(description='City-level division.\nIncludes cities, suburbs, towns and villages.\nRequires existence of continent, country and state.', example='Batie')
})

report = api.model('WHO Report', {
	'diseases': fields.List(fields.String(description='Associated diseases as specified by disease_list.json.\nIf no diseases are found, this will be an empty array.', example='Yellow fever')),
	'syndromes': fields.List(fields.String(description='Associated syndromes as specified by syndrome_list.json in project specifications.\nIf no syndromes are found, this will be an empty array.', example='Fever of unknown Origin')),
	'event_date': fields.String(description='The date(s) on which the case occured.\nDefaults to article date of publication if none is provided for the report.\nFormat is either an exact date (regex: ^(\d{4})-(\d\d|xx)-(\d\d|xx) (\d\d|xx):(\d\d|xx):(\d\d|xx)$),\nor date range (regex: ^(\d{4})-(\d\d|xx)-(\d\d|xx) (\d\d|xx):(\d\d|xx):(\d\d|xx) to (\d{4})-(\d\d|xx)-(\d\d|xx) (\d\d|xx):(\d\d|xx):(\d\d|xx)$).', example='2005-09-22 xx:xx:xx'),
	'locations': fields.List(fields.Nested(location))
})

article = api.model('WHO Article', {
	'url': fields.String(description='The url of the article.', example='https://www.who.int/csr/don/2005_09_22/en/'),
	'date_of_publication': fields.String(description='The date the article was published.\nFormat is an exact date (regex: ^(\d{4})-(\d\d|xx)-(\d\d|xx) (\d\d|xx):(\d\d|xx):(\d\d|xx)$).', example='2005-09-22 xx:xx:xx'),
	'headline': fields.String(description='The headline of the article.', example='Yellow fever in Burkina Faso and Côte d\'Ivoire'),
	'main_text': fields.String(description='The main body of the article text.', example='WHO has received reports of an outbreak of yellow fever in Batie, Gaoua and Banfora districts in Burkina Faso in the southeast of the country, near the border with Côte d\'Ivoire. Four cases including 1 death have been laboratory confirmed by Centre Muraz, Burkina Faso and by the WHO Collaborating Centre for Yellow Fever, the Institut Pasteur, Dakar, Senegal. The fatal case, a boy of 4 years old, came from Bouna region in Côte d\'Ivoire. A team from the Ministry of Health and WHO in Burkina Faso and a team from the Ministry of Health, WHO and UNICEF in Côte d\'Ivoire quickly investigated the outbreak in this cross border area characterized by increased population movements. A mass vaccination campaign is being prepared in both countries to protect the population at risk and to prevent the spread of the disease to densely populated urban settings. The WHO Regional Office for Africa is working with both Ministries to determine the most appropriate strategies for disease control in the cross border area and to raise funds for outbreak response activities.'),
	'reports': fields.List(fields.Nested(report))
})


@api.route('/articles', doc={'description': 'Retrieve articles according to parameters specified in body.'}) 
class Articles(Resource): 

	@api.response(400, 'Malformed request', error)
	@api.marshal_list_with(article, code=200)
	@api.expect(query, validate=True)
	def put(self):
		# Extra data validation	
		query = self.parse(api.payload)
		print(query)

		# TODO Query database + fetch result
		# print(sample_who_response)
		result = db_query(query)
		result.sort(key=lambda x: x['date_of_publication'])
		return result


	prog = re.compile('^[^,]*,[^,]*,[^,]*,[^,]*$')
	def parse(self, payload):
		def validate_date(date_text, error_message):
			try:
				return datetime.strptime(date_text, '%Y-%m-%d')
			except ValueError:
				api.abort(400, error_message)

		# Check dates are in correct format 
		start_date = validate_date(payload['start_date'], "Format of 'start_date' is invalid")
		end_date = validate_date(payload['end_date'], "Format of 'end_date' is invalid")

		# Check dates are ordered 
		if end_date < start_date:
			api.abort(400, "'end_date' must not precede 'start_date'")

		result = {
			'start_date': start_date,
			'end_date': end_date
		}

		# Parse key terms into array 
		if 'key_terms' in payload: 
			if payload['key_terms'].strip() == '':
				result['key_terms'] = []
			else:
				temp = payload['key_terms'].lower().split(',')
				result['key_terms'] = []
				for term in temp: 
					result['key_terms'].append(term.strip())
				
		# Parse location 
		if 'location' in payload:
			try:
				if not re.match(self.prog, payload['location']):
					raise ValueError
				categories = ['continent', 'country', 'state', 'city']
				split = payload['location'].lower().split(',')
				split = list(map(lambda x: x.strip(), split))
				result['location'] = dict(zip(categories, split))
			except: 
				api.abort(400, 'Format of \'location\' is invalid')

		logging.info('Results of query: ' + json.dumps(result, indent=4, sort_keys=True, default=str))
		return result