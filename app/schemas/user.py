from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        ..., min_length=8, description="Password must be at least 8 characters long"
    )


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    is_verified: bool
