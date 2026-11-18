from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.core.security import hash_password,    verify_password
from app.core.token_utils import create_access_token
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




def login_user_service(
    db: Session,
    email: str,
    password: str
):
    # Step 1: Find user by email
    user = get_user_by_email(db, email)

    # Step 2: Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Step 3: Verify password
    is_password_valid = verify_password(
        password,
        user.password_hash
    )

    if not is_password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Step 4: Generate access token
    access_token = create_access_token(user.id)

    # Step 5: Return token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }