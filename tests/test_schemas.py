from datetime import datetime, timezone
import pytest

from pydantic import ValidationError
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse


class FakeTask:
    id = 1
    title = "Learn FastAPI"
    description = "Learn Pydantic"
    is_completed = False
    priority = "High"
    category = "Study"
    created_at = datetime.now(timezone.utc)


def test_valid_task_creation():
    task = TaskCreate(
        title="Learn FastAPI",
        description="Practice Pydantic",
        priority="High",
        category="Study"
    )

    assert task.title == "Learn FastAPI"
    assert task.priority == "High"


def test_invalid_priority_rejected():
    with pytest.raises(ValidationError):
        TaskCreate(
            title="Learn SQLAlchemy",
            priority="Urgent",
            category="Study"
        )


def test_empty_title_rejected():
    with pytest.raises(ValidationError):
        TaskCreate(
            title="",
            category="Work"
        )


def test_partial_task_update():
    update_data = TaskUpdate(priority="Low")

    assert update_data.model_dump(
        exclude_unset=True
    ) == {"priority": "Low"}


def test_task_response_from_attributes():
    task = FakeTask()

    response = TaskResponse.model_validate(task)

    assert response.id == 1
    assert response.title == "Learn FastAPI"