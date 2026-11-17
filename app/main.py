from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.endpoints.tasks import router as tasks_router
from app.core.config import settings

app = FastAPI(
    title="TaskFlow Pro API",
    description="Backend API for TaskFlow Pro",
    version="1.0.0",
)

app.include_router(
    tasks_router,
    prefix=settings.API_V1_PREFIX
)

@app.get("/")
def root():
    return {
        "message": "TaskFlow Pro API is running"
    }


@app.get("/db-test")
def session_check(connection:Session=Depends(get_db)):
        return{"session received"}
