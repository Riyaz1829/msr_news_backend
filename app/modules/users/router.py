from app.core.security import (
    get_current_user,
    verify_password,
    hash_password
)
from app.modules.users.schemas import ChangePasswordRequest
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.security import get_current_user

from app.modules.users.models import User

from app.modules.users.schemas import (
    UserProfileResponse,
    UserProfileUpdate
)

from app.modules.users import repository

from app.modules.auth.schemas import (
    ForgotPasswordRequest,
    ResetPasswordRequest
)

from app.modules.auth.service import (
    forgot_password,
    reset_password
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# GET USER PROFILE
@router.get(
    "/profile",
    response_model=UserProfileResponse
)
def get_profile(
    current_user: User = Depends(get_current_user)
):

    return current_user


# UPDATE USER PROFILE
@router.put(
    "/profile",
    response_model=UserProfileResponse
)
def update_profile(
    user_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    update_data = user_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    if (
        "full_name" in update_data
        and update_data["full_name"] is None
    ):
        raise HTTPException(
            status_code=400,
            detail="Full name cannot be null"
        )

    if "mobile_number" in update_data:

        mobile_number = update_data["mobile_number"]

        if mobile_number is None:
            raise HTTPException(
                status_code=400,
                detail="Mobile number cannot be null"
            )

        existing_user = repository.get_user_by_mobile(
            db,
            mobile_number
        )

        if (
            existing_user
            and existing_user.id != current_user.id
        ):
            raise HTTPException(
                status_code=409,
                detail="Mobile number already registered"
            )

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user

# CHANGE PASSWORD API
@router.post("/change-password")
def change_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Verify current password
    if not verify_password(
        password_data.current_password,
        current_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Hash new password
    new_hashed_password = hash_password(
        password_data.new_password
    )

    # Update password in database
    current_user.password = new_hashed_password

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Password changed successfully"
    }
# Forgot Password API
@router.post("/forgot-password")
async def forgot_password_route(
    user_data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    return await forgot_password(db, user_data)

# Reset Password API
@router.post("/reset-password")
def reset_password_route(
    user_data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    return reset_password(db, user_data)

