from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time



app = FastAPI()

#define request body schema

class Course(BaseModel):
    name : str
    instructor: str
    duration: float
    website: HttpUrl


while True:
    try:
        conn = psycopg2.connect(host ="localhost", database = "postgres", user = 'Mazhar', password = password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Successfully connected Database')
        break
    except Exception as error:
        print('Database connection failed')
        print("Error:", error)
        time.sleep(2)


@app.post("/post")
def create_post(post: Course):
    return{"data": post}



@app.get("/")
def main_fun():
    return{"Django": "Api"}

@app.get("/course")
def study():
    return {"Course": "django & Backend api development with python"}

@app.get("/django/api")
def django():
    return {"Type": "Basic to advanced"}


