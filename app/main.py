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
from .routes_to import users as u
from .routes_to import posts as p
from .routes_to import auth 


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(p.router)
app.include_router(u.router)
app.include_router(auth.router)


# Entry Page
@app.get("/")
def message():
    
    return {"Message":"Hello World!",
            "Made By":"Devansh Mohata"}

