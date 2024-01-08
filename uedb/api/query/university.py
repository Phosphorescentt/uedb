from typing import List

from db.model.university import (
    University,
    UniversityRead,
)
from db.utils import get_session
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session


class UniversitySearch(BaseModel):
    name: str


router = APIRouter()


@router.post("/universities/search/", response_model=List[UniversityRead])
def search_university(query: UniversitySearch, session: Session = Depends(get_session)):
    search = UniversitySearch.model_validate(query)
    search_response = University.search(search.name, session)
    return search_response
