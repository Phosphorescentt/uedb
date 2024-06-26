from contextlib import contextmanager

from sqlmodel import Session, SQLModel, create_engine

# TODO: Load these from config
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@contextmanager
def get_session_context_manager():
    with Session(engine) as session:
        yield session
