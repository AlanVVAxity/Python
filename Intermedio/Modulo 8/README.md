# Módulo 08 — Arquitectura Hexagonal

Proyecto práctico del módulo intermedio de Arquitectura Hexagonal (Puertos y Adaptadores).

## Objetivo

Construir un servicio de órdenes con:

- Dominio, aplicación e infraestructura separados.
- Caso de uso `CreateOrder`.
- Puertos para persistencia y notificaciones.
- Adaptadores de repositorio en memoria y SQLAlchemy.
- API HTTP con FastAPI.
- Pruebas unitarias, de contrato, integración y end-to-end.

## Requisitos

- Python 3.12
- Poetry

## Instalación

```bash
poetry install