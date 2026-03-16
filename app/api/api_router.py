from fastapi import APIRouter

from app.api.routes import (
    auth,
    health,
    organizations,
    organizations_invitations,
    projects,
    subscriptions,
    users,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(organizations.router)
api_router.include_router(organizations_invitations.router)
api_router.include_router(projects.router)
api_router.include_router(subscriptions.router)
