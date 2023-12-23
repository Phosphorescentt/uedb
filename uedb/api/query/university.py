from typing import List

from db.model.university import (
    University,
    UniversityCreate,
    UniversityRead,
)
from db.utils import get_session
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select


class UniversitySearch(BaseModel):
    name: str


router = APIRouter()


@router.post("/universities/search/", response_model=List[UniversityRead])
def search_university(query: UniversitySearch, session: Session = Depends(get_session)):
    search = UniversitySearch.model_validate(query)
    search_response = University.search(search.name, session)
    return search_response


@router.post("/universities/", response_model=UniversityRead)
def create_university(
    university: UniversityCreate, session: Session = Depends(get_session)
):
    db_university = University.model_validate(university)
    session.add(db_university)
    session.commit()
    session.refresh(db_university)
    return db_university


@router.get("/universities/", response_model=List[UniversityRead])
def read_universities(session: Session = Depends(get_session)):
    universities = session.exec(select(University)).all()
    return universities
