from re import I
from passlib.utils.decor import deprecated_function
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List
from fastapi import FastAPI, Response, status, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import session
from sqlalchemy.sql.functions import user
from . import models, schemas, passwordhash
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Entry Page
@app.get("/")
def message():
    
    return {"Message":"Hello World!",
            "Made By":"Devansh Mohata"}


# -------------------- Posts --------------------

# Get All Posts
@app.get("/posts", response_model=List[schemas.ResponseModel])
def get_posts(db: Session = Depends(get_db)):
    
    all_posts = db.query(models.Post).all()
    return all_posts


# Get A Single Post by id
@app.get("/posts/{id}", response_model=schemas.ResponseModel)
def get_post_by_id(id:int, db: Session = Depends(get_db)):

    single_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found")

    return single_post


# Create A New Post
@app.post("/posts", response_model=schemas.ResponseModel)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

# Delete a Post by id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post_del = db.query(models.Post).filter(models.Post.id == id)

    if post_del.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found")

    post_del.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update A Post 
@app.put("/posts/{id}", response_model=schemas.ResponseModel)
def update_post(id:int, post: schemas.Post, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()



# -------------------- Users -------------------- 

# Create A User 
@app.post("/users", response_model=schemas.UserResponseModel)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    
    new_user = models.User(username = user.username, email = user.email, password = passwordhash.hashpass(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Get User Info using Username
@app.get("/users/{username}", response_model=schemas.UserResponseModel)
def get_post_by_id(username:str, db: Session = Depends(get_db)):

    user_data = db.query(models.User).filter(models.User.username == username).first()

    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with username {username} not found")

    return user_data