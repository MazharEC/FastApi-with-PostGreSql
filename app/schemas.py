from pydantic import BaseModel, HttpUrl, EmailStr
from datetime import datetime
from typing import Optional

class Course(BaseModel):
    name : str
    instructor: str
    duration: float
    website: HttpUrl


class BookCreate(BaseModel):
    name: str
    author: str
    description: str | None = None
    dept: str


class BookResponse(BookCreate):
    id: int
    creator_id : int

    class config:
        orm_model = True



class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config: 
        orm_model = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]= None
