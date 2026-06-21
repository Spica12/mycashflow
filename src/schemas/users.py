from datetime import datetime
from typing import Optional

from fastapi import File, UploadFile
from pydantic import BaseModel, EmailStr, Field, HttpUrl

from src.models.user import Roles


class RequestEmail(BaseModel):
    email: EmailStr


class UserSchema(RequestEmail):
    password: str = Field(min_length=4, max_length=20)

class CreateUserSchema(RequestEmail):
    hashed_password: str


class UserMyResponseSchema(RequestEmail):
    role: Roles
    created_at: datetime


class UserResponseSchema():
    # id: uuid.UUID
    role: Roles
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# class UserResponseExtendedSchema(UserResponseSchema):
#     picture_count: Optional[int | None]


# class UserAdminResponseSchema(UserResponseSchema, RequestEmail):
#     confirmed: bool


# class UserUpdateEmailSchema(BaseModel):
#     # Validation of user input during profile update
#     email: EmailStr = Field(max_length=255)
#     confirm_password: str = Field(max_length=255)


# class UserUpdateAvatarSchema(BaseModel):
#     # Validation of user input during profile update
#     avatar: UploadFile = File()
#     confirm_password: str = Field(max_length=255)


class UserUpdateByAdminSchema(BaseModel):
    is_active: bool = True
    role: Roles = Roles.user


# class AnotherUsers(RequestEmail, UserNameSchema):
#     # username: str
#     # email: EmailStr
#     avatar: HttpUrl | None
#     role: Roles
#     picture_count: Optional[int]
#     created_at: datetime


# class TokenSchema(BaseModel):
#     # id: int
#     access_token: str
#     refresh_token: str
#     token_type: str = "bearer"
#     # created_at: datetime
#     # updated_at: datetime


# class RequestPasswordResetSchema(BaseModel):
#     email: EmailStr
#     username: str
