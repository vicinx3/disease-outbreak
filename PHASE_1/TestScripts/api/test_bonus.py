from json import load
import os

dirname = os.path.dirname(__file__)
url = '/jhu/daily_reports'

# Test methods for bonus endpoint 
def test_get(client):
    response = client.get(url)
    assert response.status_code == 405

def test_post(client):
    response = client.get(url)
    assert response.status_code == 405

def test_delete(client):
    response = client.get(url)
    assert response.status_code == 405

# Test body 
def test_empty(client):
	response = client.put(url)
	assert response.status_code == 400
	assert response.is_json
	json = response.get_json()
	assert 'message' in json
	assert json['message'] == 'Input payload validation failed'

def test_bad_format(client):
	response = client.put(url, json='In Russia, vodka drinks you')
	assert response.status_code == 400
	assert response.is_json
	json = response.get_json()
	assert 'message' in json
	assert json['message'] == 'Input payload validation failed'

def test_missing_start_date(client):
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

def test_missing_end_date(client):
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

def test_bad_start_date(client):
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

def test_bad_end_date(client):
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

# Test expected output
def test_example(client):
	f = open(os.path.join(dirname, 'output/bonus_example.json'))
	expected = load(f)
	f.close()

	response = client.put(url, json=dict(
		start_date='2020-02-20',
		end_date='2020-03-14'
	))

	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert json == expected

def test_state_example(client):
	f = open(os.path.join(dirname, 'output/bonus_state_example.json'))
	expected = load(f)
	f.close()

	response = client.put(url, json=dict(
		start_date='2020-02-20',
		end_date='2020-03-07',
		state='hubei'
	))

	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert json == expected

def test_country_example(client):
	f = open(os.path.join(dirname, 'output/bonus_country_example.json'))
	expected = load(f)
	f.close()

	response = client.put(url, json=dict(
		start_date='2020-01-01',
		end_date='2020-02-07',
		country='MaInLaNd ChInA'
	))

	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert json == expected
