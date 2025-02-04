import pytest
# Move here from database.py
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.config import settings
from app.database import Base
import pytest
from app.oauth2 import create_access_token
from app import models


# We will not encourage to hardcode our database url here: 
# SQLALCHEMY_DATABASE_URL = f'''postgresql://postgres:e031031e@localhost:5432/fastAPI_test'''
# OR
SQLALCHEMY_DATABASE_URL = f'''postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{
    settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test'''

engine =  create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)


# Dependency to get connection or get session with database
# we just keep calling this function everytime we get requests from API endpoints
# perfrom some operations on database like get, update, delete from it
# Not longer need it, if we put this function in fixture. 
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture() 
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    # Run this before return testclient, which means before run our test
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Run the code here after we run the test

@pytest.fixture
def test_user(session, client):
    user_data = {"email": "example1@gmail.com", "password": "e031031e"}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client 

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
            "title": "first post",
            "content": "first",
            "owner_id": test_user['id']
        },{
            "title": "second post",
            "content": "2nd",
            "owner_id": test_user['id']
        },{
            "title": "third post",
            "content": "3rd",
            "owner_id": test_user['id'] 
        }]
    
    def create_posts_model(post):
        return models.Post(**post)
    
    posts_map = map(create_posts_model, posts_data)
    posts = list(posts_map)

    session.add_all(posts)
    session.commit()
    session.query(models.Post).all() # retrieving all post value
    return posts