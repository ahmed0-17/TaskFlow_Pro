from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate ,TaskUpdate
from app.repositories.task_repository import (
create_task,
get_task_by_id,
get_all_tasks,
update_task,
delete_task
)
from fastapi import HTTPException, status

def create_task_service(
    db: Session,
    task_data: TaskCreate,
    user_id: int
):
    task_dict = task_data.model_dump()

    task_dict["user_id"] = user_id

    return create_task(db, task_dict)



def get_task_service(
    db: Session,
    task_id: int,
    user_id: int
):
    task = get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=user_id
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task



def get_all_tasks_service(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
):
    return get_all_tasks(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit
    )



def update_task_service(
    db: Session,
    task_id: int,
    task_data: TaskUpdate,
    user_id: int
):
    task = get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=user_id
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    return update_task(
        db=db,
        task=task,
        task_data=update_data
    )



def delete_task_service(
    db: Session,
    task_id: int,
    user_id: int
):
    task = get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=user_id
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    delete_task(db, task)