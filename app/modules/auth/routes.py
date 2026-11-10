from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.modules.auth.schemas import (
    UserRegistration,
    UserResponse,
    UserLogin,
    TokenResponse
)

from app.modules.auth.service import (
    register_user,
    login_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# User Registration API
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def user_registration(
    user_data: UserRegistration,
    db: Session = Depends(get_db)
):

    return register_user(db, user_data)


# User Login API
@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
def user_login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):

    return login_user(db, user_data)