import pytest
import json
from application import create_app


@pytest.fixture
def client():
    client = create_app()
    return client.test_client()


def test_latest_boxoffice(client):
    response = client.get('/boxoffice/latest')
    assert response.status_code == 200
    records = json.loads(response.data)['records']
    assert records is not None and len(records) > 0
    for record in records:
        verify_boxoffice_record(record)


def verify_boxoffice_record(record):
    assert record is not None
    assert record['id'] is not None
    assert record['movieId'] is not None
    assert record['movieName'] is not None
    assert record['startDate'] is not None
    assert record['endDate'] is not None
    assert record['gross'] > 0
    assert record['theaterCount'] > 0
