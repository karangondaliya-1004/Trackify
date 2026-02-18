from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security.dependencies import get_current_user
from app.core.security.password import hash_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreateRequest, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


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


@router.get("/authorize/me")
def read_current_user(
    current_user: str = Depends(get_current_user),
):
    return {
        "message": "You are authenticated",
        "user_id": current_user,
    }
