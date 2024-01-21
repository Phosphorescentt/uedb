from typing import TYPE_CHECKING, List, Optional

from core.enums import TournamentOrganiser
from db.model.grouped_university import GroupedUniversity
from sqlmodel import Field, Relationship, Session, SQLModel, select

if TYPE_CHECKING:
    from db.model.team import Team


class UniversityBase(SQLModel):
    url: str = Field(nullable=False)
    name: str = Field(default=None)
    grouped_university_id: Optional[int] = Field(
        foreign_key="groupeduniversity.id", nullable=True
    )
    tournament_organiser: TournamentOrganiser = Field(nullable=False)
    tournament_organiser_identifier: str = Field(nullable=False)


class University(UniversityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    teams: List["Team"] = Relationship(back_populates="university")
    grouped_university: GroupedUniversity = Relationship(
        back_populates="universities",
    )

    @staticmethod
    def search(name: str, session: Session) -> List["University"]:
        universities_matching_search = session.exec(
            select(University).where(University.name.contains(name))  # type: ignore
        ).all()

        return list(universities_matching_search)


class UniversityRead(UniversityBase):
    id: int


class UniversityCreate(UniversityBase):
    ...


class UniversityUpdate(SQLModel):
    url: Optional[str] = None
    name: Optional[str] = None
    grouped_university_id: Optional[int] = None
