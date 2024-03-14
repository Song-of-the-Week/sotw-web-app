from fastapi import APIRouter

from app.api.api_v1.endpoints import auth
from app.api.api_v1.endpoints import user
from app.api.api_v1.endpoints import sotw


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(sotw.router, prefix="/sotw", tags=["sotw"])
