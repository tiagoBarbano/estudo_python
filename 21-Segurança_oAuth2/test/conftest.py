from main import app

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module", autouse=True)
def test_app():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def login_pw_token():
    return {"username": "tiago", "password": "tiago"}

@pytest.fixture(scope="module", autouse=True)
def login_pw_token_invalid():
    return {"username": "outro", "password": "outro"}