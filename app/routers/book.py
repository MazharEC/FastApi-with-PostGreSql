from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from psycopg2.extras import RealDictCursor
import time
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from .. database import get_db
from typing import List, Optional
from .. import oauth2

router = APIRouter(
    prefix="/books",
    tags = ['Book']
)

@router.post("/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    print(current_user.name)
    print(current_user.email)
    new_book = models.Book(**book.model_dump(), creator_id = current_user.id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/", response_model=List[schemas.BookResponse])
def book(db:Session = Depends(get_db),  current_user: models.User = Depends(oauth2.get_current_user), limit: int = 6, skip: int = 0, search: Optional[str]=""):
    books = db.query(models.Book).filter(models.Book.name.contains(search)).limit(limit).offset(skip).all()
    return books


@router.get("/{id}", response_model= schemas.BookResponse)
def get_book(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {id} was not found",
        )
    return book

@router.put("/{id}", response_model=schemas.BookResponse)
def update_book(id: int, updated_book: schemas.BookCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    book_query = db.query(models.Book).filter(models.Book.id == id)
    book = book_query.first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {id} does not exist",
        )
    book_query.update(updated_book.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    book_query = db.query(models.Book).filter(models.Book.id == id)
    book = book_query.first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {id} does not exist",
        )
    book_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

