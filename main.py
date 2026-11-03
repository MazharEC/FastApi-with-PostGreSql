from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from .. database import get_db
from typing import List, Optional
from .. import oauth2

app = FastAPI()

@app.get("/")
def main_fun():
    return{"Django": "Api"}

@app.get("/course")
def study():
    return {"Course": "django & Backend api development with python"}

@app.get("/django/api")
def django():
    return {"Type": "Basic to advanced"}


router = APIRouter(
    prefix="/course",
    tags = ['Course']
)

@router.post('/', response_model=schemas.CourseResponse)
def create_course(course:schemas.CourseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    print(current_user.id)
    print(current_user.email)
    new_course = models.Course(**course.model_dump(), creator_id = current_user.id)
    new_course.website = str(course.website)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course
