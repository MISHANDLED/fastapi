import psycopg2 as ps
from psycopg2.extras import RealDictCursor
from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange

from starlette.status import HTTP_204_NO_CONTENT

try:
    conn = ps.connect(host='localhost', database = 'db_api', user = 'postgres', password = 'devansh2000', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Successful")
except Exception as error:
    print(error)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Main Page
@app.get("/")
def welcome_pag():
    return {"Message" : "Hello World!"}

# Get All Posts
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"All Posts" : posts}
    
# Insert New Post
@app.post("/posts")
def post_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"New Post" : new_post}

# Find a Post by ID
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute( """SELECT * FROM posts WHERE id = %s""", (str(id)), )
    wanted_post = cursor.fetchone()
    
    if wanted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Not Possible")
    else:
        return {f"Post with id {id}": wanted_post}


@app.delete("/posts/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute( """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)), )
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Not Possible")
    
    return Response(status_code=HTTP_204_NO_CONTENT)

# Update a Post
@app.put("/posts/{id}")
def update_post(id: int, post:Post):    
    cursor.execute( """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))), )
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Not Possible")
    
    return {"Updated Post":updated_post}

