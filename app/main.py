from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.api_router import api_router
from app.core.config import config
from app.db.init_db import init_db
from app.db.session import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=config.APP_NAME, debug=getattr(config, "DEBUG", False), lifespan=lifespan
)
app.include_router(api_router)


@app.get("/")
def root():
    return {"Welcome to Multi-Tenant Subscription Billing & Usage Platform"}


@app.get("/db-check", tags=["Database"])
def db_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "Database connection successful"}
