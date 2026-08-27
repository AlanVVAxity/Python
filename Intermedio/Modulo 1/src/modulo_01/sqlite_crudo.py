"""Acceso directo a SQLite con la librería estándar, sin ORM."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path

RUTA_DB = Path(__file__).resolve().parents[2] / "data" / "crudo.db"

ESQUEMA = """
CREATE TABLE IF NOT EXISTS clientes (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email  TEXT NOT NULL UNIQUE
);
"""


def conectar() -> sqlite3.Connection:
    """Abre una conexión a la base local con filas tipo diccionario."""
    RUTA_DB.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def preparar() -> None:
    """Crea el esquema y carga datos de ejemplo."""
    with closing(conectar()) as conexion, conexion:
        conexion.executescript(ESQUEMA)
        conexion.execute("DELETE FROM clientes")
        conexion.executemany(
            "INSERT INTO clientes (nombre, email) VALUES (?, ?)",
            [
                ("Alan", "alan@example.com"),
                ("Sofia", "sofia@example.com"),
                ("Bruno", "bruno@example.com"),
            ],
        )


def listar() -> list[dict[str, object]]:
    """Devuelve todos los clientes ordenados por id."""
    with closing(conectar()) as conexion:
        filas = conexion.execute(
            "SELECT id, nombre, email FROM clientes ORDER BY id"
        ).fetchall()
        return [dict(fila) for fila in filas]


def buscar_por_email(email: str) -> dict[str, object] | None:
    """Busca un cliente por correo usando parámetros ligados."""
    with closing(conectar()) as conexion:
        fila = conexion.execute(
            "SELECT id, nombre, email FROM clientes WHERE email = ?",
            (email,),
        ).fetchone()
        return dict(fila) if fila else None


def main() -> None:
    preparar()
    for cliente in listar():
        print(cliente)
    print("Buscado:", buscar_por_email("sofia@example.com"))

    try:
        with closing(conectar()) as conexion, conexion:
            conexion.execute(
                "INSERT INTO clientes (nombre, email) VALUES (?, ?)",
                ("Duplicado", "alan@example.com"),
            )
    except sqlite3.IntegrityError as error:
        print("Rechazado por la restricción UNIQUE:", error)


if __name__ == "__main__":
    main()
