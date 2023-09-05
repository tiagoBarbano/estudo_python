import json
import pytest
from main import read_root

@pytest.mark.order(1)
def test_01(test_app):
    response = test_app.get("/hello-world")
    assert response.status_code == 200
    # assert response.json()["detail"] == "User not found"

@pytest.mark.order(2)
def test_02(test_app):
    response = read_root()
    assert response == {'Hello': 'World'}

# @pytest.mark.order(4)
# def test_create_user(test_app, monkeypatch):
#     test_request_payload = {
#                                 "nome": "tiago",
#                                 "idade": 10,
#                                 "email": "tiago@teste.com"
#                             }

#     async def mock_post(payload):
#         return 1

#     monkeypatch.setattr(repository, "add_user", mock_post)

#     response = test_app.post("/v1/user/", data=json.dumps(test_request_payload),)

#     assert response.status_code == 201
#     #assert response.json() == test_response_payload
    
# @pytest.mark.order(5)
# def test_create_user_invalid_json(test_app):
#     response = test_app.post("/v1/user/", data=json.dumps({"title": "somthing"}))
#     assert response.status_code == 422

#     response = test_app.post(
#         "/v1/user/", data=json.dumps({"title": "1", "description": "2"}))
#     assert response.status_code == 422    


# @pytest.mark.order(1)
# def test_read_user_id(test_app, monkeypatch):
#     test_data = { "id": 5, "nome": "string", "idade": 0, "email": "user@example.com"}

#     def mock_get(id):
#         return test_data

#     monkeypatch.setattr(repository, "get_user_by_id", mock_get)

#     response = test_app.get("/v1/user/5")
#     assert response.status_code == 200
#     assert response.json() == test_data
    

# @pytest.mark.order(2)
# def test_read_user_incorrect_id(test_app):
#     response = test_app.get("/v1/user/999")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "User not found"


# @pytest.mark.order(3)
# def test_read_all_users(test_app, monkeypatch):
#     def mock_get_all():
#         return None

#     monkeypatch.setattr(repository, "get_all_users", mock_get_all)

#     response = test_app.get("/v1/user/")
#     assert response.status_code == 200
    