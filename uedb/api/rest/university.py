from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db.model.university import (
    University,
    UniversityCreate,
    UniversityRead,
    UniversityUpdate,
)
from db.utils import get_session

router = APIRouter(prefix="/university")


@router.get("/id/{id}", response_model=UniversityRead)
def get_university(id: int, session: Session = Depends(get_session)):
    university = session.get(University, id)
    return university


@router.get("/list", response_model=List[UniversityRead])
def list_universities(session: Session = Depends(get_session)):
    universities = session.exec(select(University)).all()
    return universities


@router.post("/create", response_model=UniversityRead)
def create_university(
    university: UniversityCreate, session: Session = Depends(get_session)
):
    db_university = University.model_validate(university)
    session.add(db_university)
    session.commit()
    session.refresh(db_university)
    return db_university


@router.patch("/update/{university_id}", response_model=UniversityRead)
def update_university(
    university_id: int,
    university: UniversityUpdate,
    session: Session = Depends(get_session),
):
    db_university = session.get(University, university_id)
    if not db_university:
        return f"No university with id {university_id}"

    university_data = university.model_dump(exclude_unset=True)
    for key, value in university_data.items():
        setattr(db_university, key, value)

    session.add(db_university)
    session.commit()
    session.refresh(db_university)
    return db_university
