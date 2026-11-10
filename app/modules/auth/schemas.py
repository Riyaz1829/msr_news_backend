from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    model_validator
)

from typing import Self


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

    # Validate password and confirm password
    @model_validator(mode="after")
    def validate_password(self) -> Self:

        if self.password != self.confirm_password:
            raise ValueError(
                "Password and confirm password do not match"
            )

        return self


# API response schema
class UserResponse(BaseModel):

    id: int
    full_name: str
    mobile_number: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8
        )
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"