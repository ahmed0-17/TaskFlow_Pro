from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import (
create_task_service,
get_task_service,
get_all_tasks_service,
update_task_service,
delete_task_service
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task_endpoint(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    return create_task_service(
        db=db,
        task_data=task_data
    )



@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK
)
def get_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db)
):
    return get_task_service(
        db=db,
        task_id=task_id
    )



@router.get(
    "/",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK
)
def get_all_tasks_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_all_tasks_service(
        db=db,
        skip=skip,
        limit=limit
    )



@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK
)
def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    return update_task_service(
        db=db,
        task_id=task_id,
        task_data=task_data
    )



@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db)
):
    delete_task_service(
        db=db,
        task_id=task_id
    )
