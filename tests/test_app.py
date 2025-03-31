# tests/test_app.py
import pytest
from app import app as flask_app

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "ENVIRONMENT": "testing"
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_hello_world(client):
    response = client.get('/')
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'Hello DevOps World!'
    assert data['status'] == 'success'

def test_health(client):
    response = client.get('/health')
    data = response.get_json()
    assert response.status_code == 200
    assert data['status'] == 'healthy'