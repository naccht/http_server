import pytest
from api.app import app

# At the moment I'm just checking if the endpoints at least work,
# I'll add test to check if the response formatting is correct and 
# I'll use a local mock server instead of the real Exponea one

def test_all():
    """
    Test that the /api/all endpoint responds as expected
    """
    flask_app = app
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/all')
        assert response.status_code == 200

def test_first():
    """
    Test that the /api/first endpoint responds as expected
    """
    flask_app = app
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/first')
        assert response.status_code == 200
        
