from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.networks import EmailStr
from typing import List


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
    votes_count: int

    class Config:
        orm_mode = True


class Votes(BaseModel):
    post_id: int
    dir: int = Field(..., gt=-1, le=1)