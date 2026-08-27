# Módulo 05 — Principios SOLID aplicados en Python

Proyecto práctico del nivel intermedio sobre aplicación de principios SOLID en Python.

## Objetivo

Implementar un servicio de pedidos desacoplado de los detalles de persistencia mediante un puerto de repositorio y adaptadores intercambiables.

El proyecto contiene dos implementaciones de repositorio:

- `InMemoryOrderRepository`: almacena los pedidos en memoria.
- `SQLiteOrderRepository`: almacena los pedidos en una base de datos SQLite.

## Estructura del proyecto

```text
src/modulo_05/
├── domain/
│   └── order.py
├── application/
│   ├── ports.py
│   └── order_service.py
└── infrastructure/
    ├── in_memory_order_repository.py
    └── sqlite_order_repository.py