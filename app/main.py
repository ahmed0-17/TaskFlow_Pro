from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.endpoints.tasks import router as tasks_router
from app.api.v1.endpoints.auth import router as auth_router
from app.core.config import settings
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter
from app.core.exceptions import validation_exception_handler, global_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="TaskFlow Pro API",
    description="Backend API for TaskFlow Pro",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://task-flow-gilt-psi.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)





app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.include_router(
    tasks_router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    auth_router,
    prefix=settings.API_V1_PREFIX
)

@app.get("/db-test")
def session_check(connection:Session=Depends(get_db)):
        return{"session received"}
