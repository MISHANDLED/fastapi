from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app import schemas
from ..database import get_db
from .. import models, passwordhash, oauth
from sqlalchemy import or_

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

#Login 
@router.post("/", response_model=schemas.TokenBase)
def get_posts(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    info = db.query(models.User).filter(models.User.email == user_cred.username).first()

    info = db.query(models.User).filter(
        or_(
            models.User.email == user_cred.username,
            models.User.username == user_cred.username
            )
        ).first()
    
    if not info:
        raise HTTPException(status_code = HTTP_403_FORBIDDEN, detail = "Invalid Email Address")

    if not passwordhash.verifypass(user_cred.password, info.password):
        raise HTTPException(status_code = HTTP_403_FORBIDDEN, detail = "Incorrect Password")
    
    access_token = oauth.create_access_token(data={'user_id':info.id})
    return {"access_token":access_token,
            "token_type":"bearer"}