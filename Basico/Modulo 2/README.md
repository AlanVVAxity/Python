## Módulo 2: Fundamentos del lenguaje

Proyecto para practicar fundamentos de Python mediante un procesador de empleados.

### Temas aplicados

- Variables, tipos de datos y colecciones (`list`, `dict`, `set`, `tuple`).
- Comprensiones de listas y conjuntos.
- Condicionales, ciclos `for` y acumuladores.
- Funciones, alcance local y anotaciones de tipo.
- Pattern matching con `match` / `case`.
- Manejo de excepciones con `try` / `except`.
- Validación básica de correos electrónicos con expresiones regulares.
- Carga y exportación de archivos JSON.
- Logging de eventos y errores.
- Pruebas unitarias con pytest.
- Formateo y análisis estático con Black, isort, Ruff y pre-commit.

### Ejecución

```bash
poetry run python -m modulo_02.main
```

### Pruebas de Calidad
poetry run pytest
poetry run black --check src tests
poetry run isort --check-only src tests
poetry run ruff check src tests
poetry run pre-commit run --all-files
