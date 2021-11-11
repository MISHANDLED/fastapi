from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

scheme_oauth = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = 'eyJpc3MiOiAiaHR0cDovL3d3dy5leGFtcGxlLmNvbSIsICJzdWIiOiA0MiwgImV4cCI6IDEzOTU2NzQ0Mjd9'
ALGORITHM = "HS256"
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

def get_curr_user(token: str = Depends(scheme_oauth)):
    exception_details = HTTPException(
                                        status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail="Invalid credentials", 
                                        headers={"WWW-Authenticate":"Bearer"}
                                    )

    return verify_access_token(token,exception_details)

