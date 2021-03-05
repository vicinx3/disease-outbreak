# Test body for valid endpoint
url = '/who/articles'

# Empty body => malformed request 
def test_empty(client):
	response = client.put(url)
	assert response.status_code == 400
	assert response.is_json
	json = response.get_json()
	assert 'message' in json
	assert json['message'] == 'Input payload validation failed'

# Not json => malformed request 
def test_bad_format(client):
	response = client.put(url, json='In Russia, vodka drinks you')
	assert response.status_code == 400
	assert response.is_json
	json = response.get_json()
	assert 'message' in json
	assert json['message'] == 'Input payload validation failed'

def test_start_date_missing(client):
	response = client.put(url, json=dict(
		end_date='2019-05-30'
	))
	assert response.status_code == 400
	assert response.is_json
	json = response.get_json()
	assert 'message' in json
	assert json['message'] == 'Input payload validation failed'
	assert b'start_date' in response.data
	assert b'required property' in response.data

def test_end_date_missing(client):
	response = client.put(url, json=dict(
		start_date='2019-05-30'
	))
	assert response.status_code == 400
	assert response.is_json
	json = response.get_json()
	assert 'message' in json
	assert json['message'] == 'Input payload validation failed'
	assert b'end_date' in response.data 
	assert b'required property' in response.data

def test_start_date_bad(client):
	start_dates = [
		'russian vodka',
		'2019-05F30',
		'2019-13-05',
		'2019-00-05',
		'2019-02-29',
		'2020-02-30',
		'2020-07-00',
		'2020-07-32'
	]

	for start_date in start_dates:
		response = client.put(url, json=dict(
			start_date=start_date,
			end_date='2020-03-14'
		))
		assert response.status_code == 400
		assert response.is_json
		json = response.get_json()
		assert 'message' in json
		assert json['message'] == 'Format of \'start_date\' is invalid'

def test_end_date_bad(client):
	end_dates = [
		'russian vodka',
		'2019-05F30',
		'2019-13-05',
		'2019-00-05',
		'2019-02-29',
		'2020-02-30',
		'2020-07-00',
		'2020-07-32'
	]

	for end_date in end_dates:
		response = client.put(url, json=dict(
			start_date='2018-03-14', 
			end_date=end_date
		))
		assert response.status_code == 400
		assert response.is_json
		json = response.get_json()
		assert 'message' in json
		assert json['message'] == 'Format of \'end_date\' is invalid'

def test_dates_unordered(client):
	pairs = [
		('2020-02-29', '2020-02-01'),
		('2020-03-01', '2020-02-29'),
		('2018-07-31', '2003-11-10')
	]

	for pair in pairs: 
		response = client.put(url, json=dict(
			start_date=pair[0],
			end_date=pair[1]
		))
		assert response.status_code == 400
		assert response.is_json
		json = response.get_json()
		assert 'message' in json 
		assert json['message'] == '\'end_date\' must not precede \'start_date\''

# Test location formatting 
def test_location_empty_string(client):
	response = client.put(url, json=dict(
		start_date='2020-02-20',
		end_date='2020-03-07',
		location=''
	))
	assert response.status_code == 400
	assert response.is_json
	json = response.get_json()
	assert 'message' in json 
	assert json['message'] == 'Format of \'location\' is invalid'

def test_location_bad(client):
	locations = [
		'allstars',
		',',		
		',,',
		',,,,',
		',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
		'some,',
		',body',
		'one,,',
		',told,',
		',,me',
		'the,word,',
		'is,,gonna',
		',roll,me',
		'i,ain\'t,the',
		'sharpest,,,,',
		',tool,,,',
		',,in,,',
		',,,the,',
		',,,,shed',
		'she,was,,,',
		'looking,,kind,,',
		'of,,,dumb,',
		'with,,,,her',
		',finger,and,,',
		',her,,thumb,',
		',in,,,the',
		',,shape,of,',
		',,an,,L',
		',,,on,her',
		'forehead,,,,',
	]

	for location in locations:
		response = client.put(url, json=dict(
			start_date='2020-02-20',
			end_date='2020-03-07',
			location=location 
		))
		assert response.status_code == 400
		assert response.is_json
		json = response.get_json()
		assert 'message' in json 
		assert json['message'] == 'Format of \'location\' is invalid'

		