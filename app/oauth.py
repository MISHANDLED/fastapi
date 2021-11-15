from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm.session import Session
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import ENV_VALS

scheme_oauth = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = ENV_VALS.SECRET_KEY
ALGORITHM = ENV_VALS.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    encoded_data = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_data


def verify_access_token(token: str, exception_details):

    try:
        to_decode = jwt.decode(token=token,key=SECRET_KEY,algorithms=[ALGORITHM])
        id: str = to_decode.get('user_id')
        
        if id is None:
            raise exception_details

        token_data = schemas.TokenData(id=id)
        

    except JWTError:
        raise exception_details
    
    return token_data

def get_curr_user(token: str = Depends(scheme_oauth), db: Session = Depends(database.get_db)):
    exception_details = HTTPException(
                                        status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail="Invalid credentials", 
                                        headers={"WWW-Authenticate":"Bearer"}
                                    )

    token = verify_access_token(token,exception_details)
    user_details = db.query(models.User).filter(models.User.id == token.id).first()

    return user_details

