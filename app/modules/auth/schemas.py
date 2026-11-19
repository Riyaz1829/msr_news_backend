
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    model_validator
)

from typing import Self


# User Registration Schema
class UserRegistration(BaseModel):

    full_name: str = Field(
        min_length=3,
        max_length=100
    )

    mobile_number: str = Field(
        min_length=10,
        max_length=15,
        pattern=r"^[0-9]+$"
    )

    email: EmailStr

    password: str = Field(
        min_length=8
    )

    confirm_password: str

    @model_validator(mode="after")
    def validate_password(self) -> Self:

        if self.password != self.confirm_password:
            raise ValueError(
                "Password and confirm password do not match"
            )

        return self


# User Response Schema
class UserResponse(BaseModel):

    id: int
    full_name: str
    mobile_number: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


# User Login Schema
class UserLogin(BaseModel):

    identifier: str = Field(
        min_length=3,
        max_length=255
    )

    password: str = Field(
        min_length=8
    )


# Token Response Schema
class TokenResponse(BaseModel):

    access_token: str
    token_type: str = "bearer"


# Forgot Password Schema
class ForgotPasswordRequest(BaseModel):

    email: EmailStr


# Reset Password Schema
class ResetPasswordRequest(BaseModel):

    reset_token: str

    new_password: str = Field(
        min_length=8
    )

    confirm_new_password: str

    @model_validator(mode="after")
    def validate_passwords(self) -> Self:

        if self.new_password != self.confirm_new_password:
            raise ValueError(
                "New password and confirm password do not match"
            )

        return self


# OTP Send Schema
class OTPSendRequest(BaseModel):

    mobile_number: str = Field(
        min_length=10,
        max_length=15,
        pattern=r"^[0-9]+$"
    )
