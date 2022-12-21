import json
import pytest
from app import repository


def test_read_user_id(test_app, monkeypatch):
    test_data = { "id": 5, "nome": "string", "idade": 0, "email": "user@example.com"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(repository, "get_user_by_id", mock_get)

    response = test_app.get("/v1/user/5")
    assert response.status_code == 200
    assert response.json() == test_data
    
def test_read_user_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(repository, "get_user_by_id", mock_get)

    response = test_app.get("/v1/user/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_read_all_users(test_app, monkeypatch):
    async def mock_get_all():
        return None

    monkeypatch.setattr(repository, "get_all_users", mock_get_all)

    response = test_app.get("/v1/user/")
    assert response.status_code == 200
    