url = '/who/articles'

# Test date ranges 
def test_date_range(client):
	response = client.put(url, json=dict(
		start_date='2003-12-20',
		end_date='2004-01-10'
	))
	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert len(json) == 7 
	urls = list(map(lambda x: x['url'], json))
	assert set(urls) == set([
		'https://www.who.int/csr/don/2003_12_23/en/',
		'https://www.who.int/csr/don/2003_12_28/en/',
		'https://www.who.int/csr/don/2003_12_30/en/',
		'https://www.who.int/csr/don/2004_01_05/en/',
		'https://www.who.int/csr/don/2004_01_06/en/',
		'https://www.who.int/csr/don/2004_01_07/en/',
		'https://www.who.int/csr/don/2004_01_08/en/'
	])

def test_date_range1(client):
	response = client.put(url, json=dict(
		start_date='2020-02-20',
		end_date='2020-02-20'
	))
	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert len(json) == 2
	urls = list(map(lambda x: x['url'], json))
	assert set(urls) == set([
		'https://www.who.int/csr/don/20-february-2020-lassa-fever-nigeria/en/',
		'https://www.who.int/csr/don/20-february-2020-ebola-drc/en/'
	])

def test_date_range2(client):
	response = client.put(url, json=dict(
		start_date='2000-08-24',
		end_date='2000-09-10'
	))
	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert len(json) == 4
	urls = list(map(lambda x: x['url'], json))
	assert set(urls) == set([
		'https://www.who.int/csr/don/2000_08_24b/en/',
		'https://www.who.int/csr/don/2000_08_24/en/',
		'https://www.who.int/csr/don/2000_08_24a/en/',
		'https://www.who.int/csr/don/2000_09_08/en/'
	])

def test_date_range3(client):
	response = client.put(url, json=dict(
		start_date='1996-04-27',
		end_date='1996-05-03'
	))
	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert len(json) == 2
	urls = list(map(lambda x: x['url'], json))
	assert set(urls) == set([
		'https://www.who.int/csr/don/1996_04_30/en/',
		'https://www.who.int/csr/don/1996_05_03/en/'
	])

# Test keywords 
def test_key_words(client):
	response = client.put(url, json=dict(
		start_date='2012-08-29',
		end_date='2012-09-04',
		key_terms=''
	))
	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert len(json) == 4
	urls = list(map(lambda x: x['url'], json))
	assert set(urls) == set([
		'https://www.who.int/csr/don/2012_08_30a/en/',
		'https://www.who.int/csr/don/2012_08_30/en/',
		'https://www.who.int/csr/don/2012_09_03/en/',
		'https://www.who.int/csr/don/2012_09_04/en/'
	])


def test_key_words1(client):
	response = client.put(url, json=dict(
		start_date='2018-08-14',
		end_date='2018-09-20',
		key_terms='Yellow fever'
	))
	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert len(json) == 2
	urls = list(map(lambda x: x['url'], json))
	assert set(urls) == set([
		'https://www.who.int/csr/don/24-august-2018-yellow-fever-french-guiana/en/',
		'https://www.who.int/csr/don/7-september-2018-yellow-fever-congo/en/'
	])

def test_key_words2(client):
	response = client.put(url, json=dict(
		start_date='2012-10-08',
		end_date='2012-11-22',
		key_terms='Ebola, dengue'
	))
	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert len(json) == 4
	urls = list(map(lambda x: x['url'], json))
	assert set(urls) == set([
		'https://www.who.int/csr/don/2012_10_17/en/',
		'https://www.who.int/csr/don/2012_10_08a/en/',
		'https://www.who.int/csr/don/2012_10_26/en/',
		'https://www.who.int/csr/don/2012_11_17/en/'
	])

# Test location 
def test_location(client):
	response = client.put(url, json=dict(
		start_date='2008-08-08',
		end_date='2008-09-10',
		location=',,,'
	))
	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert len(json) == 3
	urls = list(map(lambda x: x['url'], json))
	assert set(urls) == set([
		'https://www.who.int/csr/don/2008_09_10a/en/',
		'https://www.who.int/csr/don/2008_09_10/en/',
		'https://www.who.int/csr/don/2008_08_08/en/'
	])

def test_location1(client):
	response = client.put(url, json=dict(
		start_date='2014-10-10',
		end_date='2014-11-13',
		location=',Uganda,,'
	))
	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert len(json) == 2
	urls = list(map(lambda x: x['url'], json))
	assert set(urls) == set([
		'https://www.who.int/csr/don/10-october-2014-marburg/en/',
		'https://www.who.int/csr/don/13-november-2014-marburg/en/'
	])

# Test keywords + location
def test_all(client):
	response = client.put(url, json=dict(
		start_date='2004-08-19',
		end_date='2004-09-29',
		key_terms='Cholera',
		location=',Chad,,'
	))
	assert response.status_code == 200
	assert response.is_json
	json = response.get_json()
	assert len(json) == 3
	urls = list(map(lambda x: x['url'], json))
	assert set(urls) == set([
		'https://www.who.int/csr/don/2004_09_01/en/',
		'https://www.who.int/csr/don/2004_09_27/en/',
		'https://www.who.int/csr/don/2004_09_27a/en/'
	])
