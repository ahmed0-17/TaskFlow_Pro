
from sqlalchemy.orm import Session
from app.models import Task


def create_task(
    db: Session,
    task_data: dict
) -> Task:

    new_task = Task(**task_data)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_task_by_id(
    db: Session,
    task_id: int,
    user_id: int
) -> Task | None:

    return (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id
        )
        .first()
    )


def get_all_tasks(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> list[Task]:

    return (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_task(
    db: Session,
    task: Task,
    task_data: dict
) -> Task:

    for field, value in task_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task
) -> None:

    db.delete(task)
    db.commit()
