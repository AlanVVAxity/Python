import os

os.environ["DATABASE_URL"] = "sqlite+pysqlite://"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-with-enough-characters"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from orders_service.infrastructure.db.base import Base
from orders_service.infrastructure.db.session import get_db_session
from orders_service.main import app


@pytest.fixture
def db_session() -> Session:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    testing_session_local = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )

    session = testing_session_local()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def client_app(db_session: Session):
    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    yield app

    app.dependency_overrides.clear()
