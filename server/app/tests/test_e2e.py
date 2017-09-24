import pytest
import app


@pytest.fixture
def client():
    app.api.testing = True
    return app.api.test_client()


def test_can_fetch_posts(client):
    res = client.get('/api/posts')
    assert res.status_code == 200
