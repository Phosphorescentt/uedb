from fastapi import APIRouter
from . import university

routers = [university.router]

query_router = APIRouter(prefix="/query", tags=["querying"])

for r in routers:
    query_router.include_router(r)
