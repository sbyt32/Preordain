from fastapi import APIRouter
from .info.router import info_router

api_router_v2 = APIRouter()

api_router_v2.include_router(info_router, prefix="/info")
