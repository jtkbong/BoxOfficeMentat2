import pytest
import json
from application import create_app


@pytest.fixture
def client():
    client = create_app()
    return client.test_client()


def test_credits_for_movie(client):
    response = client.get('/credits/marvel2019')
    assert response.status_code == 200
    credits = json.loads(response.data)['credits']
    assert credits is not None and len(credits) > 0
    for credit in credits:
        verify_credit(credit)


def verify_credit(credit):
    assert credit is not None
    assert credit['personId'] is not None
    assert credit['name'] is not None
    assert credit['relationship'] is not None
