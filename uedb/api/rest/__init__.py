from fastapi import APIRouter

from . import grouped_university, university

routers = [university.router, grouped_university.router]

rest_router = APIRouter(prefix="/rest", tags=["rest"])

for r in routers:
    rest_router.include_router(r)
