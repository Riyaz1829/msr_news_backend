
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.auth.schemas import UserRegistration, UserLogin
from app.modules.users import repository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


# User Registration
def register_user(
    db: Session,
    user_data: UserRegistration
):

    # Check existing email
    existing_email = repository.get_user_by_email(
        db,
        user_data.email
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Check existing mobile number
    existing_mobile = repository.get_user_by_mobile(
        db,
        user_data.mobile_number
    )

    if existing_mobile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mobile number already registered"
        )

    # Convert schema to dictionary
    user_dict = user_data.model_dump(
        exclude={"confirm_password"}
    )

    # Hash password
    user_dict["password"] = hash_password(
        user_data.password
    )

    # Save user in database
    new_user = repository.create_user(
        db,
        user_dict
    )

    # IMPORTANT: Return the created user
    return new_user


# User Login
def login_user(
    db: Session,
    user_data: UserLogin
):

    user = repository.get_user_by_email(
        db,
        user_data.email
    )

    if not user or not verify_password(
        user_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
