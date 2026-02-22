from enum import Enum


class OrgRole(str, Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"
