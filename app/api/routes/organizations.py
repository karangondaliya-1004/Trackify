from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants.roles import OrgRole
from app.core.security.dependencies import get_current_user
from app.core.security.org_dependencies import require_org_owner
from app.db.session import get_db
from app.models.organization import Organization
from app.models.organization_membership import OrganizationMembership
from app.models.user import User
from app.schemas.organization import (
    OrganizationCreateRequest,
    OrganizationResponse,
)

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
        .filter(Organization.owner_id == current_user.id)
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
