from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.networks import EmailStr
from sqlalchemy.sql.sqltypes import String
from typing import List
from app.database import Base

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponseModel(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True


class Post(PostBase):
    pass


class ResponseModel(PostBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class TokenBase(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str


class ResponseNew(BaseModel):
    username: str
    id: int
    title: str
    content: str 
    created_at: datetime

    class Config:
        orm_mode = True

class Response_All(BaseModel):
    __root__: List[ResponseNew]