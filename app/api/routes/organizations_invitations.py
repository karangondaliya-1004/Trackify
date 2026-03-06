from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security.dependencies import get_current_user
from app.db.session import get_db
from app.models.organization_invitation import OrganizationInvitation
from app.models.organization_membership import OrganizationMembership
from app.models.user import User

router = APIRouter(prefix="/organizations/invitations", tags=["Invitations"])


@router.post("/{invitation_id}/accept", status_code=status.HTTP_200_OK)
def accept_invitation(
    invitation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    invitation = (
        db.query(OrganizationInvitation)
        .filter(OrganizationInvitation.id == invitation_id)
        .first()
    )

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    if invitation.email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This invitation does not belong to you",
        )

    existing_membership = (
        db.query(OrganizationMembership)
        .filter(
            OrganizationMembership.organization_id == invitation.organization_id,
            OrganizationMembership.user_id == current_user.id,
        )
        .first()
    )

    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this organization",
        )

    membership = OrganizationMembership(
        organization_id=invitation.organization_id,
        user_id=current_user.id,
        role=invitation.role,
    )

    db.add(membership)
    db.delete(invitation)
    db.commit()

    return {
        "message": "Invitation accepted successfully",
        "organization_id": str(membership.organization_id),
        "role": membership.role,
    }
