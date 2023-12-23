from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from uedb.enums import TournamentOrganiser

if TYPE_CHECKING:
    from db.model.team import Team


class TournamentBase(SQLModel):
    name: str = Field(nullable=False)
    tourmament_organiser: TournamentOrganiser = Field(nullable=False)
    slug: Optional[str] = Field(default=None, unique=True)


class Tournament(TournamentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    teams: List["Team"] = Relationship(back_populates="tournament")
