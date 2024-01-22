from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from db.model.tournament import Tournament
from db.model.university import University


class TeamBase(SQLModel):
    name: str = Field(nullable=False)
    tournament_organiser_slug: Optional[str] = Field(default=None)
    tournament_organiser_id: str = Field(nullable=False)
    university_id: int = Field(nullable=False, foreign_key="university.id")


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    university: University = Relationship(back_populates="teams")
    # tournament: Tournament = Relationship(back_populates="teams")


class TeamRead(TeamBase):
    id: int


class TeamCreate(TeamBase):
    ...


class TeamUpdate(SQLModel):
    name: Optional[str] = None
    tournament_organiser_slug: Optional[str] = None
    tournament_organiser_id: Optional[int] = None
    university_id: Optional[int] = None
