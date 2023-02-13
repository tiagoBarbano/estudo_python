from jose import jwt
from app.utils.config import get_settings

settings = get_settings()


def test_login_user(test_app, login_pw_token):
    res = test_app.post("/v1/security/token", data=login_pw_token)  
    login_res = res.json()
    payload = jwt.decode(login_res['access_token'], settings.secret_key, algorithms=[settings.algorithm])
    sub = payload.get("sub")

    assert sub == "tiago"
    assert res.status_code == 200


def test_login_user_invalid(test_app, login_pw_token_invalid):
    res = test_app.post("/v1/security/token", data=login_pw_token_invalid)
    
    assert res.status_code == 400
    assert res.json() == {"detail":"Incorrect username or password"}    
    

def test_get_users(test_app, login_pw_token):  
    res = test_app.post("/v1/security/token", data=login_pw_token)
    login_res = res.json()    
    response = test_app.get("/v1/user/teste", headers={"token": login_res['access_token']})

    assert response.status_code == 200
