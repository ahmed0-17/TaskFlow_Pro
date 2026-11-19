from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.token_utils import verify_access_token
from app.repositories.user_repository import get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    
    user_id = verify_access_token(token)

   
    user = get_user_by_id(db, user_id)

    if user is None:
     raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found",
        headers={"WWW-Authenticate": "Bearer"}
    )


    if not user.is_active:
     raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Your account is inactive"
    )


    return user