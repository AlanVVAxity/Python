# Módulo 06 — Librería estándar y E/S

## Objetivo

Desarrollar una aplicación de consola en Python que lea un archivo CSV de ventas, valide la información, calcule métricas, genere un resumen JSON y registre la ejecución mediante logging.

## Funcionalidades

- Lectura de archivos CSV mediante `csv.DictReader`.
- Validación de campos obligatorios, enteros, decimales y fechas.
- Uso de `Decimal` para cálculos monetarios.
- Uso de fechas ISO 8601 con zona horaria.
- Cálculo de métricas de ventas.
- Exportación de resultados a JSON.
- Manejo de rutas con `pathlib.Path`.
- Registro de eventos, advertencias y errores con `logging`.
- Verificación del intérprete de Python con `subprocess`.
- Pruebas automatizadas con pytest.

## Estructura del proyecto

```text
modulo-06/
├── data/
│   └── ventas.csv
├── logs/
│   └── modulo_06.log
├── output/
│   └── resumen_ventas.json
├── src/
│   └── modulo_06/
├── tests/
├── pyproject.toml
└── README.md
