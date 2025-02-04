# Provide the test flow, like login, create user, create post, vote for post, get the post......
import pytest
from app import schemas
from jose import jwt
from app.config import Settings

settings = Settings()

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World'
    assert res.status_code  == 200

# We can testing this like this, or using below alternative way
# def test_create_user():
#     res = client.post("/users", json = {"email": "example1@gmail.com", "password": "e031031e"})
#     print(res.json())
#     assert res.json().get("email") == "example1@gmail.com"
#     assert res.status_code == 201

# This function will directly test our userOut model, which validate our user gmail, password and created time. 
def test_create_user(client):
    res = client.post("/users/", json = {"email": "example1@gmail.com", "password": "e031031e"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "example1@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data = {"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrong@gmail.com', 'password123', 403),
    ('wrong2@gmail.com', 'password12', 403),
    ('example1@gmail.com', 'e031031e', 403)  
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code

# Testing for reading function
def test_get_all_posts(authorized_client, test_user):
    res = authorized_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200 



