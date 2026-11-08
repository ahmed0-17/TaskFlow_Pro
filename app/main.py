from fastapi import FastAPI

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
