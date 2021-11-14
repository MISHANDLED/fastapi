from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .. import oauth

router = APIRouter(
    prefix="/posts",
    tags=["POSTS"]
)

# Get All Posts
@router.get("/", response_model=schemas.Response_All)
def get_posts(db: Session = Depends(get_db)):

    all_posts = db.query(models.Post, models.User).filter(models.Post.user_id == models.User.id).with_entities(
        models.User.username, models.Post.id, models.Post.title, models.Post.content, models.Post.created_at
        ).all() 
    
    
    return all_posts


# Get A Single Post by id
@router.get("/{id}", response_model=schemas.ResponseNew)
def get_post_by_id(id:int, db: Session = Depends(get_db)):

    single_post = db.query(models.Post, models.User).filter(models.Post.user_id == models.User.id).with_entities(
        models.User.username, models.Post.id, models.Post.title, models.Post.content, models.Post.created_at
        ).first()

    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found")

    return single_post


# Create A New Post
@router.post("/", response_model=schemas.ResponseModel)
def create_post(post: schemas.Post, db: Session = Depends(get_db), user_details: int = Depends(oauth.get_curr_user)):
    
    # print(user_details)
    
    new_post = models.Post(title=post.title, content=post.content, published=post.published, user_id = user_details.id)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

# Delete a Post by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_details: int = Depends(oauth.get_curr_user)):

    # print(user_details)
    
    post_del = db.query(models.Post).filter(models.Post.id == id)

    if post_del.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found")

    if post_del.first().user_id != user_details.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"You're not the owner of this post")

    post_del.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update A Post 
@router.put("/{id}", response_model=schemas.ResponseModel)
def update_post(id:int, post: schemas.Post, db: Session = Depends(get_db), user_details: int = Depends(oauth.get_curr_user)):

    # print(user_details)
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found")

    if post_query.first().user_id != user_details.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"You're not the owner of this post")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
