from typing import List, Optional

from sqlmodel import Field, Session, SQLModel, select


class UniversityBase(SQLModel):
    slug: str = Field()
    name: str = Field()

    @staticmethod
    def search(name: str, session: Session) -> List["UniversityTable"]:
        universities_matching_search = session.exec(
            select(UniversityTable).where(UniversityTable.name.contains(name))  # type: ignore
        ).all()

        return list(universities_matching_search)


class UniversityTable(UniversityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UniversityDeserialise(UniversityBase):
    pass


class UniversitySerialise(UniversityBase):
    id: int
