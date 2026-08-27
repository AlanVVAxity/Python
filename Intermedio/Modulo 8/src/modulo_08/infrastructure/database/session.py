from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from modulo_08.infrastructure.database.base import Base


def create_database_engine(database_url: str) -> Engine:
    return create_engine(database_url, echo=False)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def create_database_tables(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)
