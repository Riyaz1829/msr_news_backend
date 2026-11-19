
from pydantic import BaseModel, EmailStr, Field
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    model_validator
)


# User Profile Response
class UserProfileResponse(BaseModel):

    id: int
    full_name: str
    mobile_number: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


# User Profile Update
class UserProfileUpdate(BaseModel):

    full_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    mobile_number: str | None = Field(
        default=None,
        min_length=10,
        max_length=15,
        pattern=r"^[0-9]+$"
    )

# Change Password Request Schema
class ChangePasswordRequest(BaseModel):

    current_password: str = Field(
        min_length=8
    )

    new_password: str = Field(
        min_length=8
    )

    confirm_new_password: str

    @model_validator(mode="after")
    def validate_password(self):

        if self.new_password != self.confirm_new_password:
            raise ValueError(
                "New password and confirmation do not match"
            )

        if self.current_password == self.new_password:
            raise ValueError(
                "New password must be different from current password"
            )

        return self

