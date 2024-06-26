from fastapi import APIRouter

from . import team, university

routers = [university.router, team.router]

ingestion_router = APIRouter(prefix="/ingest", tags=["ingestion triggers"])

for r in routers:
    ingestion_router.include_router(r)
