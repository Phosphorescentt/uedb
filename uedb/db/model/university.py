from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Session, SQLModel, select, Relationship

if TYPE_CHECKING:
    from db.model.team import Team


class UniversityBase(SQLModel):
    slug: str = Field(default=None)
    name: str = Field(default=None)


class University(UniversityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    teams: List["Team"] = Relationship(back_populates="university")

    def get_teams(self) -> List["Team"]:
        return self.teams

    @staticmethod
    def search(name: str, session: Session) -> List["University"]:
        universities_matching_search = session.exec(
            select(University).where(University.name.contains(name))  # type: ignore
        ).all()

        return list(universities_matching_search)


class UniversityCreate(UniversityBase):
    ...


class UniversityRead(UniversityBase):
    id: int
