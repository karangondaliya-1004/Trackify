from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import config
from app.db.session import get_db

router = APIRouter(tags=["Health"])


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Health check endpoint.

    Verifies:
    - Service is running
    - Database connection is healthy
    """
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "unhealthy"

    return {
        "status": "ok",
        "database": db_status,
        "environment": config.__class__.__name__,
        "service": "trackify",
        "message": "Service is running",
    }
