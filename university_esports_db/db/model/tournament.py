from uedb.enums import TournamentOrganiser
from typing import Optional
from sqlmodel import SQLModel, Field


class TournamentBase(SQLModel):
    name: str = Field(nullable=False)
    tourmament_organiser: TournamentOrganiser = Field(nullable=False)
    slug: Optional[str] = Field(default=None)


class Tournament(TournamentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ...
