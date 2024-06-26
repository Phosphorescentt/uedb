from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, Session, SQLModel, select

if TYPE_CHECKING:
    from db.model.university import University

    pass


class GroupedUniversityBase(SQLModel):
    name: str = Field(default=None, unique=True)


class GroupedUniversity(GroupedUniversityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    universities: List["University"] = Relationship(back_populates="grouped_university")

    @staticmethod
    def search(name: str, session: Session) -> List["GroupedUniversity"]:
        grouped_universities_matching_search = session.exec(
            select(GroupedUniversity).where(GroupedUniversity.name.contains(name))  # type: ignore
        ).all()

        return list(grouped_universities_matching_search)


class GroupedUniversityRead(GroupedUniversityBase):
    id: int


class GroupedUniversityCreate(GroupedUniversityBase):
    ...


class GroupedUniversityUpdate(SQLModel):
    name: Optional[str] = None
    ...
