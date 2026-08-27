"""Configuración del módulo, tomada de variables de entorno."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_DATOS = RAIZ_PROYECTO / "data"


@dataclass(frozen=True)
class Settings:
    """Ajustes de conexión del módulo."""

    database_url: str
    sql_echo: bool


@lru_cache
def get_settings() -> Settings:
    """Devuelve los ajustes activos (memorizados)."""
    RUTA_DATOS.mkdir(parents=True, exist_ok=True)
    url_por_defecto = f"sqlite+pysqlite:///{(RUTA_DATOS / 'modulo_08.db').as_posix()}"
    return Settings(
        database_url=os.getenv("DATABASE_URL", url_por_defecto),
        sql_echo=os.getenv("SQL_ECHO", "0") == "1",
    )
