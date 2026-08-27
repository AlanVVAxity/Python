from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from modulo_01.config import get_settings

URL_MEMORIA = "sqlite+pysqlite:///:memory:"


def crear_engine(url: str | None = None, *, echo: bool | None = None) -> Engine:
    """Crea un engine listo para usar, con SQLite configurado correctamente."""
    settings = get_settings()
    url_final = url or settings.database_url
    opciones: dict[str, Any] = {
        "echo": settings.sql_echo if echo is None else echo,
    }

    if ":memory:" in url_final:
        opciones["connect_args"] = {"check_same_thread": False}
        opciones["poolclass"] = StaticPool

    engine = create_engine(url_final, **opciones)

    if engine.dialect.name == "sqlite":

        @event.listens_for(engine, "connect")
        def _activar_llaves_foraneas(dbapi_connection: Any, _: Any) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


def crear_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Devuelve una fábrica de sesiones ligada al engine indicado."""
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)


@contextmanager
def sesion_de(engine: Engine) -> Iterator[Session]:
    """Abre una sesión, confirma al salir y revierte si hubo error."""
    factory = crear_session_factory(engine)
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
