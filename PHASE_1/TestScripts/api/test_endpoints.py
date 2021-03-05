# Test invalid endpoints 

def test_home(client):
    url = '/'
    response = client.get(url)
    assert response.status_code == 200
    assert b'Codeonavirus' in response.data

    response = client.post(url)
    assert response.status_code == 405

    response = client.put(url)
    assert response.status_code == 405

    response = client.delete(url)
    assert response.status_code == 405

def test_incorrect(client):
    urls = [
        '/who',
        '/who/article',
        '/some/endpoint'
    ]
    for url in urls: 
        response = client.get(url)
        assert response.status_code == 404
        assert b'The requested URL was not found on the server' in response.data
        
        response = client.post(url)
        assert response.status_code == 404
        assert b'The requested URL was not found on the server' in response.data
        
        response = client.put(url)
        assert response.status_code == 404
        assert b'The requested URL was not found on the server' in response.data
        
        response = client.delete(url)
        assert response.status_code == 404
        assert b'The requested URL was not found on the server' in response.data

# Test queries with valid endpoint
def test_queries(client):
    response = client.put('/who/articles/?vodka=russia')
    assert response.status_code == 404