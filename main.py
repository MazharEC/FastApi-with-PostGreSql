from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main_fun():
    return{"Django": "Api"}