from fastapi import APIRouter
from . import grouped_university

routers = [grouped_university.router]

management_router = APIRouter(prefix="/management", tags=["management"])

for r in routers:
    management_router.include_router(r)
