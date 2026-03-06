from pydantic import BaseModel, EmailStr

from app.core.constants.roles import OrgRole


class OrganizationInviteCreateRequest(BaseModel):
    email: EmailStr
    role: OrgRole = OrgRole.MEMBER
