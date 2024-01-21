from typing import List

from db.model.grouped_university import (
    GroupedUniversity,
    GroupedUniversityCreate,
    GroupedUniversityRead,
)
from db.utils import get_session
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

router = APIRouter(prefix="/grouped_university")


@router.get("/list/", response_model=List[GroupedUniversityRead])
def read_grouped_universities(session: Session = Depends(get_session)):
    grouped_universities = session.exec(select(GroupedUniversity)).all()
    print(grouped_universities)
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
