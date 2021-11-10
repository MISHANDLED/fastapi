from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "Mr.", "content": "Devansh","id":999},
    {"title": "Mr.", "content": "Devansh","rating":5,"id":99},
]

def find_post(id):
    for post in my_posts:
        if  post['id'] == id:
            return post

def getpostindex(id):
    for i, post in enumerate(my_posts):
        if post['id'] ==id:
            return i


# Main Page 
@app.get("/")
def read_root():
    return {"Message": "Hello World!"}


# Gets all posts 
@app.get("/posts")
def read_root():
    return {"Message": my_posts}


# Add a post 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def send_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1,1000000)
    my_posts.append(post_dict)
    return "Done"


# Get a Particular Post via Post ID
@app.get("/posts/{id}")
def get_id(id: int, response: Response):
    post_find = find_post(id)
    
    if not post_find:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found")

    return {'data': post_find}



# Delete a Post
@app.delete("/posts/{id}")
def delete_post(id: int):
    index = getpostindex(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Post with id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a Post
@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = getpostindex(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Post with id {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return{"Message":"Updated The Required Post"}


# @app.post("/createpost")
# async def ok(post: dict = Body(...)):
#     print(post)
#     return "Done"

