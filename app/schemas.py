from pydantic import BaseModel
from datetime import datetime
from pydantic.networks import EmailStr
from sqlalchemy.sql.sqltypes import String

from app.database import Base

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class Post(PostBase):
    pass

class ResponseModel(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponseModel(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class LoginBase(BaseModel):
    email: EmailStr
    password = str


    