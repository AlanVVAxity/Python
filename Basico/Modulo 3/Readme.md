## Módulo 3: Funciones y programación pythonic

Proyecto para practicar funciones reutilizables y patrones idiomáticos de Python mediante una simulación de envío de notificaciones en lotes.

### Temas aplicados

- Funciones con parámetros posicionales y nombrados.
- Uso de `*args` y `**kwargs`.
- Closures para conservar configuraciones de formateo.
- Generadores con `yield`.
- Tipado genérico con `TypeVar`.
- Decoradores parametrizables.
- Reintentos ante errores temporales con backoff.
- Preservación de metadatos de funciones con `functools.wraps`.
- Context managers implementados con `__enter__` y `__exit__`.
- Medición de rendimiento con `time.perf_counter`.
- Logging y manejo de excepciones.
- Pruebas unitarias con pytest y `monkeypatch`.
- Automatización de calidad con Black, isort, Ruff y pre-commit.

### Ejecución

```bash
poetry run python -m modulo_03.main
```

### PRUEBAS DE CALIDAD
poetry run pytest
poetry run black --check src tests
poetry run isort --check-only src tests
poetry run ruff check src tests
poetry run pre-commit run --all-files
