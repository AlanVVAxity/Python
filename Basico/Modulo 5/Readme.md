# Módulo 5: Tipado estático y calidad

Proyecto práctico del módulo 5 del nivel básico de la guía de Python.

## Objetivo

Implementar una aplicación simple de gestión de tareas utilizando:

- Anotaciones de tipos.
- `Literal` para estados y prioridades.
- `TypedDict` para entradas y actualizaciones.
- `Protocol` para definir el contrato del repositorio.
- `dataclass` para representar una tarea.
- `mypy` para análisis estático.
- `ruff`, `black` e `isort` para calidad y formato.
- `pytest` para pruebas automatizadas.
- `pre-commit` para automatizar validaciones antes de cada commit.

## Estructura

```text
src/modulo_05/
├── main.py
├── models.py
├── repository.py
└── service.py

tests/
├── test_models.py
├── test_repository.py
└── test_service.py
