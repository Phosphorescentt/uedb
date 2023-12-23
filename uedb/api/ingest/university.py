from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel


class UniversitySearch(BaseModel):
    name: str
    use_external: Optional[bool]


router = APIRouter()


@router.post("/universities")
def ingest_university() -> None:
    ...
