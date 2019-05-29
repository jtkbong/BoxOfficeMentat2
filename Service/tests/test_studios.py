import pytest
import json
from application import create_app


@pytest.fixture
def client():
    client = create_app()
    return client.test_client()


def test_get_studio(client):
    response = client.get('/studios/warnerbros')
    assert response.status_code == 200
    studio = json.loads(response.data)
    verify_studio(studio)


def test_non_existent_studio(client):
    assert client.get('/studios/NotRealStudio').status_code == 404


def test_get_studios(client):
    response = client.get('/studios')
    assert response.status_code == 200
    studios = json.loads(response.data)['studios']
    for studio in studios:
        verify_studio(studio)


def test_get_studios_max_results(client):
    response = client.get('/studios?maxResults=20')
    assert response.status_code == 200
    studios = json.loads(response.data)['studios']
    assert len(studios) == 20


def verify_studio(studio):
    assert studio is not None
    assert studio['id']
    assert studio['name']
    if len(studio) == 3:
        assert studio['count'] >= 0
