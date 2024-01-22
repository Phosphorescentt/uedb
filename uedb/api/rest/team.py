from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db.model.team import Team, TeamCreate, TeamRead, TeamUpdate
from db.utils import get_session

router = APIRouter(prefix="/team")


@router.get("/id/{id}", response_model=TeamRead)
def get_team(id: int, session: Session = Depends(get_session)):
    team = session.get(Team, id)
    return team


@router.get("/list", response_model=List[TeamRead])
def list_teams(session: Session = Depends(get_session)):
    teams = session.exec(select(Team)).all()
    return teams


@router.get("/create", response_model=TeamRead)
def create_team(team: TeamCreate, session: Session = Depends(get_session)):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.get("/update/{team_id}", response_model=TeamRead)
def update_team(
    team_id: int, team: TeamUpdate, session: Session = Depends(get_session)
):
    db_team = session.get(Team, id)
    if not db_team:
        return f"No Team with id {team}"

    team_data = team.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)

    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team
