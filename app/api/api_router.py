from fastapi import APIRouter

from app.api.routes import auth, health, organizations, organizations_invitations, users

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(organizations.router)
api_router.include_router(organizations_invitations.router)
