from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional 

# Using pydantic to perform typecasting, which valid our output datatypes. 

# Defining a input data schema, define the structure of user input to us
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # default as true

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

# Defining the schema or structure of how we response to user
class Post(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    owner: UserOut
    # published: bool
    # created_at: datetime
    # To tell our sqlalchemy ignore our response data is dictionary, convert it to json and response
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str 

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class vote(BaseModel):
    post_id: int
    # Restrict that only the integar less than 1, which is 0 or 1 is allowed
    dir: int = Field(..., le=1)

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        from_attributes = True


