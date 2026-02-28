import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from app.core.constants.invitations import InvitationStatus
from app.core.constants.roles import OrgRole
from app.db.base import Base


class OrganizationInvitation(Base):
    __tablename__ = "organization_invitations"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    organization_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )

    email = Column(String, nullable=False)

    role = Column(
        Enum(OrgRole, name="org_invite_role_enum"),
        nullable=False,
    )

    invited_by_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    token = Column(String, unique=True, nullable=False)

    status = Column(
        Enum(InvitationStatus, name="org_invite_status_enum"),
        default=InvitationStatus.PENDING,
        nullable=False,
    )

    expires_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    accepted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="invitations")
    invited_by = relationship(
        "User",
        back_populates="sent_invitations",
    )

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "email",
            name="uq_org_pending_invite_email",
        ),
    )
