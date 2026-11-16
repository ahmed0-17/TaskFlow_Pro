import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime, timezone
from app.schemas.task import TaskCreate,TaskUpdate,TaskResponse
from pydantic import ValidationError


class FakeTask:
    id = 1
    title = "Learn FastAPI"
    description = "Learn Pydantic"
    is_completed = False
    priority = "High"
    category = "Study"
    created_at = datetime.now(timezone.utc)


task = FakeTask()

response = TaskResponse.model_validate(task)

print(response.model_dump(mode="json"))






# Test 1: Valid task
task_data = TaskCreate(
    title="Learn FastAPI",
    description="Practice Pydantic",
    priority="High",
    category="Study"
)

print("Valid task:", task_data.model_dump(mode="json"))


# Test 2: Invalid priority
try:
    TaskCreate(
        title="Learn SQLAlchemy",
        priority="Urgent",
        category="Study"
    )
except ValidationError as error:
    print("Invalid priority rejected!")


# Test 3: Empty title
try:
    TaskCreate(
        title="",
        category="Work"
    )
except ValidationError:
    print("Empty title rejected!")


# Test 4: Partial update
update_data = TaskUpdate(
    priority="Low"
)

print(
    "Partial update:",
    update_data.model_dump(exclude_unset=True , mode="json")
)