from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.core.security.dependencies import get_active_membership, require_org_role
from app.db.session import get_db
from app.models.organization_membership import OrganizationMembership
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "",
    response_model=ProjectResponse,
)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    membership: OrganizationMembership = Depends(require_org_role(["OWNER", "ADMIN"])),
):

    project = Project(
        name=project_in.name,
        description=project_in.description,
        organization_id=membership.organization_id,
        created_by=membership.user_id,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def list_projects(
    db: Session = Depends(get_db),
    membership: OrganizationMembership = Depends(
        require_org_role(["OWNER", "ADMIN", "MEMBER"])
    ),
):

    projects = (
        db.query(Project)
        .filter(
            Project.organization_id == membership.organization_id,
            Project.deleted_at.is_(None),
        )
        .order_by(Project.created_at.desc())
        .all()
    )

    return projects


def validate_project_in_active_org(
    project_id: UUID,
    db: Session = Depends(get_db),
    membership: OrganizationMembership = Depends(get_active_membership),
):
    """
    Fetch project and validate it belongs to active organization.
    """

    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.deleted_at.is_(None))
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    if project.organization_id != membership.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to this project is forbidden",
        )

    return project


@router.get("/{project_id}")
def get_project(
    project: Project = Depends(validate_project_in_active_org),
):
    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    membership: OrganizationMembership = Depends(get_active_membership),
):

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.organization_id == membership.organization_id,
            Project.deleted_at.is_(None),
        )
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.deleted_at = func.now()

    db.commit()
    db.refresh(project)
    return {"message": "Project deleted"}
