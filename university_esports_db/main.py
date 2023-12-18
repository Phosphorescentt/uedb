from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select


class UniversityBase(SQLModel):
    slug: str = Field()
    name: str = Field()

    @staticmethod
    def search(name: str, session: Session) -> List["UniversityTable"]:
        with Session(engine) as session:
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


class UniversitySearch(BaseModel):
    name: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/universities/search/", response_model=List[UniversitySerialise])
def search_university(query: UniversitySearch):
    search = UniversitySearch.model_validate(query)
    with Session(engine) as session:
        search_response = UniversityBase.search(search.name, session)
        return search_response


@app.post("/universities/", response_model=UniversitySerialise)
def create_university(university: UniversityDeserialise):
    db_university = UniversityTable.model_validate(university)
    with Session(engine) as session:
        session.add(db_university)
        session.commit()
        session.refresh(db_university)
        return db_university


@app.get("/universities/", response_model=List[UniversitySerialise])
def read_universities():
    with Session(engine) as session:
        universities = session.exec(select(UniversityTable)).all()
        return universities
