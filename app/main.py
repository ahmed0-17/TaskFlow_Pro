from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from app.core.database import get_db


app = FastAPI(
    title="TaskFlow Pro API",
    description="Backend API for TaskFlow Pro",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "TaskFlow Pro API is running"
    }


@app.get("/db-test")
def session_check(connection:Session=Depends(get_db)):
        return{"session received"}
