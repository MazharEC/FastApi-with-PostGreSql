from fastapi import FastAPI


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


