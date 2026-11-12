from sqlalchemy import Column, Integer,String, Float, TIMESTAMP, text
from . database import Base

class Book(Base):
    __tablename__ = "books"
    id= Column(Integer, primary_key= True, index= True)
    name= Column(String, nullable=False)
    author= Column(String, nullable=False)
    description = Column(String, nullable=True)
    dept= Column(String, nullable=False)
    

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))