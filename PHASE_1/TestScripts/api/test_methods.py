# Test methods for valid endpoints

def test_get(client):
	response = client.get('/who/articles')
	assert response.status_code == 405
	assert response.is_json
	json = response.get_json()
	assert 'message' in json
	assert json['message'] == 'The method is not allowed for the requested URL.'

def test_post(client):
	response = client.post('/who/articles')
	assert response.status_code == 405
	assert response.is_json
	json = response.get_json()
	assert 'message' in json
	assert json['message'] == 'The method is not allowed for the requested URL.'

def test_delete(client):
	response = client.delete('/who/articles')
	assert response.status_code == 405 
	assert response.is_json
	json = response.get_json()
	assert 'message' in json
	assert json['message'] == 'The method is not allowed for the requested URL.'


	