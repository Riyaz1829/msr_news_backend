
import secrets

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.modules.auth.schemas import (
    UserRegistration,
    UserResponse,
    UserLogin,
    TokenResponse,
    OTPSendRequest
)

from app.modules.auth.service import (
    register_user,
    login_user
)

from app.services.msg91 import msg91_service
from app.services.rate_limit import check_otp_rate_limit


# Existing authentication router
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Separate OTP router
otp_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


# Send OTP API - Mock SMS with Redis Rate Limiting
@otp_router.post(
    "/otp/send",
    status_code=status.HTTP_202_ACCEPTED
)
async def send_otp(user_data: OTPSendRequest):

    # Step 1: Check OTP request limit using Redis
    allowed = await check_otp_rate_limit(
        user_data.mobile_number
    )

    # Step 2: Reject if maximum requests exceeded
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "code": "RATE_LIMIT_EXCEEDED",
                "message": "Maximum 5 OTP requests per hour exceeded."
            }
        )

    # Step 3: Generate a secure six-digit OTP
    otp = str(secrets.randbelow(900000) + 100000)

    # Step 4: Dispatch through mock MSG91 service
    try:
        result = await msg91_service.send_otp(
            mobile_number=user_data.mobile_number,
            otp=otp
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc)
        )

    # Step 5: Return API response
    return {
        "success": True,
        "data": {
            "mobile_number": user_data.mobile_number,
            "provider": result["provider"],
            "status": result["status"],
            "simulated": result["simulated"],
            "delivered": result["delivered"]
        },
        "meta": None,
        "error": None
    }


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
