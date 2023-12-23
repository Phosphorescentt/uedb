from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, Session, SQLModel, select

if TYPE_CHECKING:
    from db.model.team import Team


class UniversityBase(SQLModel):
    slug: str = Field(default=None, unique=True)
    name: str = Field(default=None)


class University(UniversityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    teams: List["Team"] = Relationship(back_populates="university")

    @staticmethod
    def search(
        name: str, session: Session, use_external: bool = False
    ) -> List["University"]:
        if not use_external:
            universities_matching_search = session.exec(
                select(University).where(University.name.contains(name))  # type: ignore
            ).all()

            return list(universities_matching_search)
        else:
            return []


class UniversityCreate(UniversityBase):
    ...


class UniversityRead(UniversityBase):
    id: int
