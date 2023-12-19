from uedb.enums import TournamentOrganiser
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from db.model.team import Team


class TournamentBase(SQLModel):
    name: str = Field(nullable=False)
    tourmament_organiser: TournamentOrganiser = Field(nullable=False)
    slug: Optional[str] = Field(default=None, unique=True)


class Tournament(TournamentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    teams: List["Team"] = Relationship(back_populates="tournament")
