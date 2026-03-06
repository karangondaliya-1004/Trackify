from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    organization_id: UUID
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True
