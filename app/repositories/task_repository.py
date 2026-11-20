from sqlalchemy.orm import Session
from app.models import Task
from sqlalchemy import asc, desc


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
    limit: int = 100,
    search: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    is_completed: bool | None = None,
    priority: str | None = None,
    category: str | None = None,
) -> list[Task]:

    query = db.query(Task).filter(
        Task.user_id == user_id
    )

    if search:
        query = query.filter(
            Task.title.ilike(f"%{search}%")
        )

    
    if is_completed is not None:
     query = query.filter(
        Task.is_completed == is_completed
    )

    if priority is not None:
     query = query.filter(
        Task.priority == priority
    )

    if category is not None:
     query = query.filter(
        Task.category == category
    )


    sort_columns = {
        "created_at": Task.created_at,
        "title": Task.title
    }

    sort_column = sort_columns[sort_by]

    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))
    

    return (
        query
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
