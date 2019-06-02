import pytest
import json
from application import create_app


@pytest.fixture
def client():
    client = create_app()
    return client.test_client()


def test_get_person(client):
    response = client.get('/person/joshbrolin')
    assert response.status_code == 200
    person_json = json.loads(response.data)
    verify_person(person_json)


def test_get_non_existent_person(client):
    assert client.get('/person/rendblackhand').status_code == 404


def test_search_chris(client):
    response = client.get('/people?name=chris&maxResults=20&offset=40')
    assert response.status_code == 200
    people = json.loads(response.data)['people']
    assert len(people) == 20
    for person in people:
        verify_person(person)


def test_count_people(client):
    response = client.get('/people?name=chris&mode=count')
    assert response.status_code == 200
    count = json.loads(response.data)['count']
    assert count > 0


def verify_person(person):
    assert person is not None
    assert person['id']
    assert person['name']
    assert person['actor'] in [0, 1]
    assert person['director'] in [0, 1]
    assert person['producer'] in [0, 1]
    assert person['screenWriter'] in [0, 1]

