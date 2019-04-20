import pytest
import json
from application import create_app
from datetime import datetime


@pytest.fixture
def client():
    client = create_app()
    return client.test_client()


def test_get_movie(client):
    assert client.get('/movie/ironman').status_code == 200


def test_get_non_existent_movie(client):
    assert client.get('/movie/ironman4').status_code == 404


def test_get_movies(client):
    response = client.get('/movies?person=robertdowneyjr&studio=SonyColumbia')
    assert response.status_code == 200
    movies = json.loads(response.data)['movies']
    assert len(movies) > 0


def test_get_movies_with_released_year(client):
    response = client.get('/movies?releaseYear=2017')
    assert response.status_code == 200
    movies = json.loads(response.data)['movies']
    for movie in movies:
        released_date = datetime.strptime(movie['releasedDate'], '%m/%d/%Y')
        assert released_date.year == 2017

