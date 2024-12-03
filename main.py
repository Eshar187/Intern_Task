from fastapi import FastAPI
from routes import *
app = FastAPI()

@app.get('/')
def root():
    return {'message':'Hello World'}

app.include_router(student_router)
