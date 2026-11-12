from fastapi import FastAPI, HTTPException, status, Response, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from sqlalchemy.orm import Session
from . database import engine, get_db
from typing import List



app = FastAPI()

models.Base.metadata.create_all(bind=engine)


while True:
    try:
        conn = psycopg2.connect(host ="localhost", database = "postgres", user = "postgres", password =pasword, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Successfully connected Database')
        break
    except Exception as error:
        print('Database connection failed')
        print("Error:", error)
        time.sleep(2)


# @app.post("/post")
# def create_post(post: Course):
#     cursor.execute("""INSERT INTO courses(name, instructor, duration, website) VALUES(%s, %s, %s, %s)""", (post.name, post.instructor, post.duration, str(post.website)))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return{"data": new_post}



# @app.get("/")
# def main_fun():
#     return{"Django": "Api"}

# @app.get("/course")
# def study():
#     return {"Course": "django & Backend api development with python"}

# @app.get("/")
# def get_table():
#     cursor.execute("""SELECT * FROM courses""")
#     data = cursor.fetchall()
#     return {"Data" : data}

# @app.get("/django/api")
# def django():
#     return {"Type": "Basic to advanced"}



# @app.get("courses/{id}")
# def get_course(id: int):
#     cursor.execute("""SELECT * FROM courses WHERE id = %s """, (str(id),))
#     courses = cursor.fetchone()
#     if not courses:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail= f"Course with id:{id} was not found"
#         )
#     return{"Course_detail": courses}


# @app.delete("/courses/{id}", status_code= status.HTTP_204_NO_CONTENT)
# def delete_course(id: int):
#     cursor.execute("""DELETE FROM courses WHERE id =%s returning * """, (str(id),))
#     deleted_course = cursor.fetchone()
#     conn.commit()
#     if deleted_course == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"course with id: {id} does not exist")
#     return Response(status_code=status.HTTP_404_NOT_FOUND)
     

# @app.put("/courses/{id}")
# def update_course(id: int, course: Course):
#     cursor.execute("""UPDATE course SET name = %s, instructor = %s, duration = %s, website = %s WHERE id= %s RETURNING * """, (course.name, course.instructor, course.duration, str(course.website), str(id)))
#     update_course = cursor.fetchone()
#     conn.commit()

#     if update_course == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id: {id} does not exist")
#     return {"data": update_course}


@app.post("/books", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books", response_model=List[schemas.BookResponse])
def book(db:Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books


@app.get("/books/{id}", response_model= schemas.BookResponse)
def get_book(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {id} was not found",
        )
    return book

@app.put("/books/{id}", response_model=schemas.BookResponse)
def update_book(id: int, updated_book: schemas.BookCreate, db: Session = Depends(get_db)):
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


@app.delete("/delete_book/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db: Session = Depends(get_db)):
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



#User table related codes start form here

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def library_user(user: schemas.UserCreate, db:Session=Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
