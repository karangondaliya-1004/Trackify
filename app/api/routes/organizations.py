import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants.roles import OrgRole
from app.core.security.dependencies import get_current_user
from app.core.security.org_dependencies import require_org_owner
from app.db.session import get_db
from app.models.organization import Organization
from app.models.organization_invitation import OrganizationInvitation
from app.models.organization_membership import OrganizationMembership
from app.models.user import User
from app.schemas.organization import (
    OrganizationCreateRequest,
    OrganizationResponse,
)
from app.schemas.organization_invitation import OrganizationInviteCreateRequest

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_organization(
    org_in: OrganizationCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_org = (
        db.query(Organization)
        .join(OrganizationMembership)
        .filter(
            Organization.name == org_in.name,
            OrganizationMembership.user_id == current_user.id,
            OrganizationMembership.role == OrgRole.OWNER,
        )
        .first()
    )

    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already own an organization with this name",
        )

    organization = Organization(name=org_in.name, owner_id=current_user.id)
    db.add(organization)
    db.flush()

    membership = OrganizationMembership(
        user_id=current_user.id,
        organization_id=organization.id,
        role=OrgRole.OWNER,
    )

    db.add(membership)
    db.commit()
    db.refresh(organization)

    return organization


@router.get(
    "",
    response_model=list[OrganizationResponse],
)
def list_organizations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    organizations = (
        db.query(Organization)
        .join(OrganizationMembership)
        .filter(OrganizationMembership.user_id == current_user.id)
        .order_by(Organization.created_at.desc())
        .all()
    )

    return organizations


@router.delete("/{organization_id}")
def delete_organization(
    organization_id: UUID,
    membership: OrganizationMembership = Depends(require_org_owner),
    db: Session = Depends(get_db),
):
    organization = membership.organization
    db.delete(organization)
    db.commit()

    return {"message": "Organization deleted successfully"}


@router.post(
    "/{organization_id}/invite",
    status_code=status.HTTP_201_CREATED,
)
def invite_user(
    organization_id: UUID,
    invite_in: OrganizationInviteCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    membership = (
        db.query(OrganizationMembership)
        .filter(
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.user_id == current_user.id,
        )
        .first()
    )

    if not membership or membership.role != OrgRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organization owners can invite users",
        )

    existing_member = (
        db.query(OrganizationMembership)
        .join(User)
        .filter(
            OrganizationMembership.organization_id == organization_id,
            User.email == invite_in.email,
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this organization",
        )

    existing_invite = (
        db.query(OrganizationInvitation)
        .filter(
            OrganizationInvitation.organization_id == organization_id,
            OrganizationInvitation.email == invite_in.email,
            OrganizationInvitation.accepted_at.is_(None),
        )
        .first()
    )

    if existing_invite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation already sent to this email",
        )

    token = secrets.token_urlsafe(32)
    invitation = OrganizationInvitation(
        organization_id=organization_id,
        email=invite_in.email,
        role=invite_in.role,
        token=token,
        invited_by_id=current_user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    return {
        "message": "Invitation sent successfully",
        "email": invitation.email,
    }


def get_active_membership(
    x_organization_id: str = Header(..., alias="X-Organization-ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Resolve active organization from request header
    and validate membership.
    """

    organization = (
        db.query(Organization).filter(Organization.id == x_organization_id).first()
    )

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    membership = (
        db.query(OrganizationMembership)
        .filter(
            OrganizationMembership.organization_id == organization.id,
            OrganizationMembership.user_id == current_user.id,
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this organization",
        )

    return membership


def require_org_role(allowed_roles: list[str]):
    """
    Dependency factory to enforce organization roles.
    """

    def role_checker(
        membership: OrganizationMembership = Depends(get_active_membership),
    ):
        if membership.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient organization permissions",
            )

        return membership

    return role_checker
