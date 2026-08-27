"""Fixtures compartidas: base de datos en memoria por prueba."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from modulo_01.db import URL_MEMORIA, crear_engine
from modulo_01.models import Base


@pytest.fixture()
def engine() -> Iterator[Engine]:
    motor = crear_engine(URL_MEMORIA, echo=False)
    Base.metadata.create_all(motor)
    yield motor
    Base.metadata.drop_all(motor)
    motor.dispose()


@pytest.fixture()
def session(engine: Engine) -> Iterator[Session]:
    with Session(engine, expire_on_commit=False) as sesion:
        yield sesion
