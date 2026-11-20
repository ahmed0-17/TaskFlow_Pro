from fastapi import Depends, status, APIRouter, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.dependencies.auth import get_current_user
from app.models import User
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_task_service(
        db=db,
        task_data=task_data,
        user_id=current_user.id
    )



@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK
)
def get_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_task_service(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )


@router.get(
    "/",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK
)
def get_all_tasks_endpoint(
    skip: int = Query(default=0,ge=0),
    limit: int = Query(default=10,ge=1,le=100),
    search: str | None = Query(default=None, min_length=1, max_length=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    sort_by: str = Query(default="created_at",pattern="^(created_at|title)$"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    is_completed: bool | None = Query(default=None),
    priority: str | None = Query(
    default=None,
    pattern="^(High|Medium|Low)$"
     ),
    category: str | None = Query(
    default=None,
    pattern="^(Personal|Work|Study|Shopping)$"
    ),
):

    return get_all_tasks_service(
        db=db,
        skip=skip,
        limit=limit,
        user_id=current_user.id,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        is_completed=is_completed,
        priority=priority,
        category=category
    )



@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK
)
def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_task_service(
        db=db,
        task_id=task_id,
        task_data=task_data,
        user_id=current_user.id
    )



@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_task_service(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )
