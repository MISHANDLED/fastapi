from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import ENV_VALS

# URL = 'postgresql://postgres:devansh2000@localhost:5432/db_api'
URL = f'postgresql://{ENV_VALS.DB_USERNAME}:{ENV_VALS.DB_PASSWORD}@{ENV_VALS.DB_HOSTNAME}:{ENV_VALS.DB_PORT}/{ENV_VALS.DB_NAME}'

engine = create_engine(URL)
sessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()