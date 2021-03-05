
# Example test 
def test_article(client):
	response = client.get('/who/articles') # GET request
	assert response.status_code == 405