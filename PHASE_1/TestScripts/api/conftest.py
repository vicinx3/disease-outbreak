import pytest 
from PHASE_1.API_SourceCode.server.app import app  

# Configuration file

# Setup Flask app for testing 
@pytest.fixture(scope='module')
def client():
	app.config['TESTING'] = True

	with app.test_client() as client:
		yield client