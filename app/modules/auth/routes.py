
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.modules.auth.schemas import (
    UserRegistration,
    UserResponse,
    UserLogin,
    TokenResponse,
    OTPSendRequest,
    OTPVerifyRequest
)

from app.modules.auth.service import (
    register_user,
    login_user
)

from app.services.msg91 import msg91_service
from app.services.rate_limit import check_otp_rate_limit
from app.services.otp_service import (
    generate_otp,
    store_otp,
    verify_otp
)


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


# Send OTP API
@otp_router.post(
    "/otp/send",
    status_code=status.HTTP_202_ACCEPTED
)
async def send_otp(user_data: OTPSendRequest):

    allowed = await check_otp_rate_limit(
        user_data.mobile_number
    )

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "code": "RATE_LIMIT_EXCEEDED",
                "message": "Maximum 5 OTP requests per hour exceeded."
            }
        )

    otp = generate_otp()

    await store_otp(
        user_data.mobile_number,
        otp
    )

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


# Verify OTP API
@otp_router.post(
    "/otp/verify",
    status_code=status.HTTP_200_OK
)
async def verify_mobile_otp(
    user_data: OTPVerifyRequest
):

    is_valid = await verify_otp(
        user_data.mobile_number,
        user_data.otp
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_OR_EXPIRED_OTP",
                "message": "Invalid or expired OTP."
            }
        )

    return {
        "success": True,
        "data": {
            "mobile_number": user_data.mobile_number,
            "verified": True,
            "message": "Mobile number verified successfully."
        },
        "meta": None,
        "error": None
    }


# User Registration API - OTP Verification Required
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def user_registration(
    user_data: UserRegistration,
    db: Session = Depends(get_db)
):
    return await register_user(db, user_data)


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
