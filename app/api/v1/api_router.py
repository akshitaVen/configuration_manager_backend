from fastapi import APIRouter
from app.api.v1.endpoints import configurations

api_v1_router = APIRouter()
api_v1_router.include_router(configurations.router, prefix="", tags=["Configurations"])
