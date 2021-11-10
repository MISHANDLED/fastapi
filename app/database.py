from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL = 'postgresql://postgres:devansh2000@localhost/db_api'

engine = create_engine(URL)
sessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()