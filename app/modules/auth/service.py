
from datetime import datetime, timedelta, timezone

import jwt

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.auth.schemas import (
    UserRegistration,
    UserLogin,
    ForgotPasswordRequest,
    ResetPasswordRequest
)

from app.modules.users import repository

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_password_reset_token
)

from app.core.config import SECRET_KEY, ALGORITHM


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

    # Save user
    new_user = repository.create_user(
        db,
        user_dict
    )

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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Forgot Password
def forgot_password(
    db: Session,
    user_data: ForgotPasswordRequest
):

    user = repository.get_user_by_email(
        db,
        user_data.email
    )

    # Do not reveal whether an email exists
    if not user:
        return {
            "message": "If the account exists, a password reset link will be sent."
        }

    # Generate password reset token
    reset_token = create_password_reset_token(
        user.id
    )

    # DEVELOPMENT ONLY:
    # Print token in terminal for Swagger testing.
    # In production, send this token through email.
    print("PASSWORD RESET TOKEN:", reset_token)

    return {
        "message": "Password reset instructions generated. Check the backend terminal."
    }


# Reset Password
def reset_password(
    db: Session,
    user_data: ResetPasswordRequest
):

    try:
        # Decode reset token
        payload = jwt.decode(
            user_data.reset_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Verify token purpose
        if payload.get("purpose") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password reset token"
            )

        user_id = int(payload.get("sub"))

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token data"
        )

    # Find user
    user = repository.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Hash new password
    user.password = hash_password(
        user_data.new_password
    )

    # Update database
    try:
        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to reset password"
        )

    return {
        "message": "Password reset successfully"
    }
