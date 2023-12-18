from typing import List

from db.utils import get_session
from db.model.university import (
    UniversityBase,
    UniversityDeserialise,
    UniversitySerialise,
    UniversityTable,
)
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select


class UniversitySearch(BaseModel):
    name: str


router = APIRouter()


@router.post("/universities/search/", response_model=List[UniversitySerialise])
def search_university(query: UniversitySearch, session: Session = Depends(get_session)):
    search = UniversitySearch.model_validate(query)
    search_response = UniversityBase.search(search.name, session)
    return search_response


@router.post("/universities/", response_model=UniversitySerialise)
def create_university(
    university: UniversityDeserialise, session: Session = Depends(get_session)
):
    db_university = UniversityTable.model_validate(university)
    session.add(db_university)
    session.commit()
    session.refresh(db_university)
    return db_university


@router.get("/universities/", response_model=List[UniversitySerialise])
def read_universities(session: Session = Depends(get_session)):
    universities = session.exec(select(UniversityTable)).all()
    return universities
