from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.repositories.user_repository import (
    get_user_by_email,
    create_user
)


def register_user_service(
    db: Session,
    user_data: UserCreate
):
    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    hashed_password = hash_password(user_data.password)

    user_data_dict = {
        "name": user_data.name,
        "email": user_data.email,
        "password_hash": hashed_password
    }

    return create_user(db, user_data_dict)