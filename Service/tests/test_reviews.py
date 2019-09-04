import pytest
import json
from application import create_app


@pytest.fixture
def client():
    client = create_app()
    return client.test_client()


def test_get_review(client):
    response = client.get('/review/spidermanhomecoming2')
    assert response.status_code == 200
    review = json.loads(response.data)
    verify_review(review)


def test_get_reviews(client):
    response = client.get('/reviews')
    assert response.status_code == 200
    reviews = json.loads(response.data)['reviews']
    verify_reviews(reviews)


def test_post_reviews(client):
    response = client.post('/reviews', data=dict(
        movieId='avatar',
        reviewText='this movie made a lot of money'
    ))
    assert response.status_code == 200


def verify_review(review):
    assert review is not None
    assert review['id']
    assert review['movieId']
    assert review['movieName']
    assert review['dateTime']
    assert review['reviewText']
    assert review['reviewStats']


def verify_reviews(reviews):
    assert reviews
    assert len(reviews) > 0
    for review in reviews:
        assert review['id']
        assert review['movieId']
        assert review['movieName']
        assert review['dateTime']
        assert review['reviewStats']
