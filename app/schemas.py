from pydantic import BaseModel
from datetime import datetime

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