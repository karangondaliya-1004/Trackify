from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import config
from app.db.session import get_db

app = FastAPI(title=config.APP_NAME, debug=getattr(config, "DEBUG", False))


@app.get("/")
def root():
    return {"Welcome to the server"}


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": config.__class__.__name__,
        "service": "saas-core",
        "message": "Service is running",
    }


@app.get("/db-check", tags=["Database"])
def db_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "Database connection successful"}
