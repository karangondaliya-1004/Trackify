from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routes.organizations import require_org_role
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
        .filter(Project.organization_id == membership.organization_id)
        .order_by(Project.created_at.desc())
        .all()
    )

    return projects
