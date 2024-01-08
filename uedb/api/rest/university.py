from typing import List

from db.model.university import University, UniversityCreate, UniversityRead
from db.utils import get_session
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

router = APIRouter(prefix="/university")


@router.get("/list/", response_model=List[UniversityRead])
def read_universities(session: Session = Depends(get_session)):
    universities = session.exec(select(University)).all()
    return universities


@router.post("/create/", response_model=UniversityRead)
def create_university(
    university: UniversityCreate, session: Session = Depends(get_session)
):
    db_university = University.model_validate(university)
    session.add(db_university)
    session.commit()
    session.refresh(db_university)
    return db_university
