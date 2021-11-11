from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, passwordhash
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["USERS"]
)

# Create A User 
@router.post("/", response_model=schemas.UserResponseModel)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    
    new_user = models.User(username = user.username, email = user.email, password = passwordhash.hashpass(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Get User Info using Username
@router.get("/{username}", response_model=schemas.UserResponseModel)
def get_post_by_id(username:str, db: Session = Depends(get_db)):

    user_data = db.query(models.User).filter(models.User.username == username).first()

    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with username {username} not found")

    return user_data


# Get User Info using ID
@router.get("/{id}", response_model=schemas.UserResponseModel)
def get_post_by_id(id:int, db: Session = Depends(get_db)):

    user_data = db.query(models.User).filter(models.User.id == id).first()

    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with username {id} not found")

    return user_data