import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from app.db.base import Base


class OrganizationSubscription(Base):
    __tablename__ = "organization_subscriptions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    organization_id = Column(
        PG_UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )

    plan_id = Column(
        PG_UUID(as_uuid=True), ForeignKey("subscription_plans.id"), nullable=False
    )

    trial_ends_at = Column(DateTime, nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
