import json
import pytest
from app import repository


def test_create_user(test_app, monkeypatch):
    test_request_payload = {
                                "nome": "tiago",
                                "idade": 10,
                                "email": "tiago@teste.com"
                            }

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(repository, "add_user", mock_post)

    response = test_app.post("/v1/user/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    #assert response.json() == test_response_payload
    
def test_create_user_invalid_json(test_app):
    response = test_app.post("/v1/user/", data=json.dumps({"title": "somthing"}))
    assert response.status_code == 422

    response = test_app.post(
        "/v1/user/", data=json.dumps({"title": "1", "description": "2"}))
    assert response.status_code == 422    
