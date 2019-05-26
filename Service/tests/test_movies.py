import pytest
import json
from application import create_app
from datetime import datetime


@pytest.fixture
def client():
    client = create_app()
    return client.test_client()


def test_get_movie(client):
    response = client.get('/movie/ironman')
    assert response.status_code == 200
    movie = json.loads(response.data)
    verify_movie(movie)


def test_get_non_existent_movie(client):
    assert client.get('/movie/ironman4').status_code == 404


def test_get_genres(client):
    response = client.get('/genres')
    assert response.status_code == 200
    genres = json.loads(response.data)['genres']
    assert len(genres) > 20


def test_get_ratings(client):
    response = client.get('/ratings')
    assert response.status_code == 200
    genres = json.loads(response.data)['ratings']
    assert len(genres) > 5


def test_get_movies(client):
    response = client.get('/movies?person=robertdowneyjr&studio=sony')
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


def verify_movie(movie):
    assert movie
    assert movie['id']
    assert movie['name']
    assert movie['studio']
    assert movie['domesticGross']
    assert movie['distributor']
    assert movie['releasedDate']
    assert movie['genre']
    assert movie['runTime']
    assert movie['mpaaRating']
    assert movie['productionBudget']
    if 'weeks' in movie:
        for week in movie['weeks']:
            assert week['weekNumber'] >= 0
            assert week['startDate']
            assert week['endDate']
            assert week['gross'] >= 1
            assert week['theaterCount'] >= 0
