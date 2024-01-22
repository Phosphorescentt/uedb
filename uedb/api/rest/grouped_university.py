from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db.model.grouped_university import (
    GroupedUniversity,
    GroupedUniversityCreate,
    GroupedUniversityRead,
    GroupedUniversityUpdate,
)
from db.utils import get_session

router = APIRouter(prefix="/grouped_university")


@router.get("/id/{id}", response_model=GroupedUniversityRead)
def get_grouped_university(id: int, session: Session = Depends(get_session)):
    grouped_university = session.get(GroupedUniversity, id)
    return grouped_university


@router.get("/list/", response_model=List[GroupedUniversityRead])
def list_grouped_universities(session: Session = Depends(get_session)):
    grouped_universities = session.exec(select(GroupedUniversity)).all()
    return grouped_universities


@router.post("/create/", response_model=GroupedUniversityRead)
def create_grouped_universities(
    grouped_university: GroupedUniversityCreate,
    session: Session = Depends(get_session),
):
    db_grouped_university = GroupedUniversity.model_validate(grouped_university)
    session.add(db_grouped_university)
    session.commit()
    session.refresh(db_grouped_university)
    return db_grouped_university


@router.patch("/update/{grouped_university_id}", response_model=GroupedUniversityRead)
def update_grouped_university(
    grouped_university_id: int,
    grouped_university: GroupedUniversityUpdate,
    session: Session = Depends(get_session),
):
    db_grouped_university = session.get(GroupedUniversity, grouped_university_id)
    if not db_grouped_university:
        return f"No university with id {grouped_university_id}"

    grouped_university_data = grouped_university.model_tump(exclude_unset=True)
    for key, value in grouped_university_data.items():
        setattr(db_grouped_university, key, value)

    session.add(db_grouped_university)
    session.commit()
    session.refresh(db_grouped_university)
    return db_grouped_university
