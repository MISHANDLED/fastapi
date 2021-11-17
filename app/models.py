from sqlalchemy.sql.expression import text, true
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "postsdata"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'True', nullable = False)
    created_at = Column(TIMESTAMP(timezone=true), nullable = False, server_default = text('now()'))  
    user_id = Column(Integer, ForeignKey("usersdata.id", ondelete="CASCADE"), nullable=False)


class User(Base):
    __tablename__ = "usersdata"

    id = Column(Integer, primary_key = True, nullable = False)
    username = Column(String, unique = True, nullable = False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=true), nullable = False, server_default = text('now()'))


class Vote(Base):
    __tablename__ = "votesdata"

    user_id = Column(Integer,ForeignKey("usersdata.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer,ForeignKey("postsdata.id", ondelete="CASCADE"), primary_key=True)