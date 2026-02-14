from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.core.security.password import hash_password
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


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


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    payload: UserCreateRequest,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == payload.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    if not payload.password.strip():
        raise HTTPException(status_code=400, detail="Password cannot be empty")

    hashed_password = hash_password(payload.password)
    user = User(
        email=payload.email,
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
