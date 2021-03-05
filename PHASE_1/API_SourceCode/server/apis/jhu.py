from flask import request 
from flask_restplus import Namespace, Resource, fields, abort 
from datetime import datetime
import logging 
import json
import os
from glob import glob
import csv
from .sample.jhu_response import sample_jhu_response
from .models import error
from ._jhu_path import path # Create this file and have a string variable (named path) that is the path of the JHU data set, or comment this file out 

api = Namespace('JHU', description='COVID-19 data provided by John Hopkins University', path='/jhu')

# Models
query = api.model('JHU Query', {
	'start_date': fields.Date(required=True, description='Required.\nStart date of date range to fetch reports from.\nNote that the earliest report provided is on 2020-01-22.\nMust be in YYYY-MM-DD format and precede end_date.', example='2020-02-20'),
	'end_date': fields.Date(required=True, description='Required.\nEnd date of date range to fetch reports from.\nMust be in YYYY-MM-DD format and succeed start_date.', example='2020-03-07'),
	'state': fields.String(description='Filter report entries by state or province, case-insensitive.\nCan be combined with \'country\'.', example='Hubei'),
	'country': fields.String(description='Filter report entries by country or region, case-insensitive.\nCan be combined with \'state\'.', example='China')
})

entry = api.model('JHU Entry', {
	'city': fields.String(description='City/Town of entry.\nNot applicable before 2020-03-22.', example='Saratoga'),
	'state': fields.String(description='State/Province of entry.', example='Hubei'),
	'country': fields.String(description='Country/Region of entry.', example='Mainland China'),
	'last_update': fields.DateTime(description='Time of last update for entry.\nFormat is \'YYYY-MM-DDThh:mm:ss\'.', example='2020-02-20T23:43:02'),
	'confirmed': fields.Integer(description='Running total of confirmed cases of COVID-19.', min=0, example='62442'),
	'deaths': fields.Integer(description='Running total of deaths from COVID-19.', min=0, example='2144'),
	'recovered': fields.Integer(description='Running total of people that have recovered from COVID-19.', min=0, example='11788'),
	'latitude': fields.String(description='Latitude of location.\nNull if not found in dataset.', example='30.9756'),
	'longitude': fields.String(description='Longitude of location.\nNull if not found in dataset', example='112.2707')
})

report = api.model('JHU Report', {
	'date': fields.Date(description='Date of report.\nFormat is \'YYYY-MM-DD\'.', example='2020-02-20'),
	'entries': fields.List(fields.Nested(entry))
})

error = api.model('Error', model=error.model)

@api.route('/daily_reports', doc={'description': 'Retrieve daily reports of COVID-19 statistics in specified date range.\nSee https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports for example of data.'})
class Daily_Reports(Resource):

	@api.response(400, 'Malformed request', error)
	@api.marshal_list_with(report, code=200)
	@api.expect(query, validate=True)
	def put(self):
		# Extra data validation
		query = self.parse(api.payload)
		print(query)

		try: 
			return self.fetch(query)
		except:
			api.abort(500, "Something went wrong with the server")

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
			'end_date': end_date,
		}

		if 'state' in payload: 
			result['state'] = payload['state'].lower()

		if 'country' in payload:
			result['country'] = payload['country'].lower()

		logging.info('Results of query: ' + json.dumps(result, indent=4, sort_keys=True, default=str))
		return result 

	def fetch(self, query):
		# Filter files within date range
		files = {datetime.strptime(os.path.basename(f).split('.')[0], r'%m-%d-%Y'): f for f in glob(path + '/*.csv')}
		for date in list(files.keys()):
			if (date < query['start_date']) or (date > query['end_date']):
				del files[date]

		# Generate result 
		result = []
		for date in sorted(list(files.keys())):
			f = open(files[date], 'r')
			reader = csv.reader(f)
			entries = []

			line_count = 0
			for row in reader:
				row_clone = row.copy()
				if line_count == 0:	# Skip first line 
					line_count += 1 
					continue
				
				# Special processing for new reports from 2020-03-22
				if date >= datetime(2020, 3, 22):
					# Optional filtering 
					if 'state' in query and query['state'] not in row_clone[2].lower().split():
						continue
					if 'country' in query and query['country'] not in row_clone[3].lower().split():
						continue
					
					standard_format = r'%Y-%m-%dT%H:%M:%S'
					pattern = r'%m/%d/%y %H:%M' if date == datetime(2020, 3, 22) else r'%Y-%m-%d %H:%M:%S' 
					temp_date = datetime.strptime(row_clone[4], pattern)
					row_clone[4] = temp_date.strftime(standard_format)

					# Defaults
					if row_clone[1] == '':
						row_clone[1] = None
					if row_clone[2] == '':
						row_clone[2] = None

					categories = ['FIPS', 'city', 'state', 'country', 'last_update', 'latitude', 'longitude', 'confirmed', 'deaths', 'recovered']
					entries.append(dict(zip(categories, row_clone)))
					continue 

				# Optional filtering 
				if 'state' in query and query['state'] not in row_clone[0].lower().split():
					continue 
				if 'country' in query and query['country'] not in row_clone[1].lower().split():
					continue 
				
				# Fix date format if before 2020-02-02
				if date < datetime(2020, 2, 2):
					standard_format = r'%Y-%m-%dT%H:%M:%S'
					pattern = r'%m/%d/%Y %H:%M'
					if date > datetime(2020, 1, 22) and date < datetime(2020, 1, 31):
						pattern = r'%m/%d/%y %H:%M'
					temp_date = datetime.strptime(row_clone[2], pattern)
					row_clone[2] = temp_date.strftime(standard_format)
				
				# Set defaults
				for i in range(3, 6):
					if row_clone[i] == '': 
						row_clone[i] = 0
				if row_clone[0] == '':
					row_clone[0] = None

				categories = ['state', 'country', 'last_update', 'confirmed', 'deaths', 'recovered', 'latitude', 'longitude']
				entries.append(dict(zip(categories, row_clone)))

			if len(entries) != 0: 
				result.append({
					'date': date.strftime(r'%Y-%m-%d'),
					'entries': entries
				})
			f.close()
		return result
