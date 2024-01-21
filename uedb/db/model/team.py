from typing import Optional

from core.enums import Game
from db.model.tournament import Tournament
from db.model.university import University
from sqlmodel import Field, Relationship, SQLModel


class TeamBase(SQLModel):
    name: str = Field(nullable=False)
    nuel_slug: Optional[str] = Field(default=None)
    nse_slug: Optional[str] = Field(default=None)
    game: Optional[Game] = Field(default=Game.VALORANT)
    university_id: int = Field(nullable=False, foreign_key="university.id")
    tournament_id: int = Field(nullable=False, foreign_key="tournament.id")


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    university: University = Relationship(back_populates="teams")
    tournament: Tournament = Relationship(back_populates="teams")
