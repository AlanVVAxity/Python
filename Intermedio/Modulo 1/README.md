# Módulo 08 — Acceso a datos y ORM

Persistencia de órdenes con SQLite, SQLAlchemy 2.0 (Core y ORM) y migraciones con Alembic.

## Contenido

- `sqlite_crudo.py`: acceso directo con `sqlite3`.
- `models/`: entidades `User`, `Order` y `OrderItem` con relaciones y restricciones.
- `repositories/`: operaciones CRUD sobre sesiones de SQLAlchemy.
- `queries.py`: consultas agregadas con ORM y con Core.
- `alembic/`: migraciones versionadas del esquema.
- `tests/`: pruebas contra SQLite en memoria.

## Requisitos

- Python 3.12+
- Poetry

## Instalación

```bash
poetry install
```

## Migrar y ejecutar

```bash
poetry run alembic upgrade head
poetry run python -m modulo_08.main
```

## Pruebas

```bash
poetry run pytest
```

## Calidad

```bash
poetry run ruff check .
poetry run ruff format .
poetry run isort --check-only .
```

## Configuración

| Variable | Valor por defecto | Uso |
|---|---|---|
| `DATABASE_URL` | `sqlite+pysqlite:///./data/modulo_08.db` | Cadena de conexión |
| `SQL_ECHO` | `0` | `1` imprime el SQL generado |
