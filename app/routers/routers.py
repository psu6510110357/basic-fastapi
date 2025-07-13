from fastapi import APIRouter
from app.routers.v1.users_router import router as users_router
from app.routers.v1.authentication_router import router as auth_router

router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(auth_router, prefix="/auth", tags=["authentication"])
