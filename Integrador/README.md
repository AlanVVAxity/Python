# Orders Service

API REST para la gestión de órdenes, construida con Python, FastAPI, PostgreSQL y SQLAlchemy.
El proyecto aplica principios de Arquitectura Hexagonal / Arquitectura Limpia, separando el dominio, casos de uso, puertos y adaptadores.

---

## Tabla de contenido

- [Orders Service](#orders-service)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Características](#características)
  - [Arquitectura](#arquitectura)
  - [Diagrama de arquitectura general](#diagrama-de-arquitectura-general)
  - [Diagrama de dependencias por capas](#diagrama-de-dependencias-por-capas)
  - [Diagrama de flujo para crear una orden](#diagrama-de-flujo-para-crear-una-orden)
  - [Diagrama de entidades de base de datos](#diagrama-de-entidades-de-base-de-datos)
  - [Diagrama de estados de una orden](#diagrama-de-estados-de-una-orden)
  - [Tecnologías](#tecnologías)
  - [| pip-audit | Auditoría de vulnerabilidades |](#-pip-audit--auditoría-de-vulnerabilidades-)
  - [Requisitos previos](#requisitos-previos)
  - [git --version](#git---version)
    - [Instalación y configuración local](#instalación-y-configuración-local)
  - [1. Clonar el repositorio](#1-clonar-el-repositorio)
  - [2. Crear el archivo de variables de entorno](#2-crear-el-archivo-de-variables-de-entorno)
  - [Copy-Item .env.example .env](#copy-item-envexample-env)
  - [3. Configurar las variables de entorno](#3-configurar-las-variables-de-entorno)
  - [JWT\_SECRET\_KEY=una\_clave\_larga\_y\_segura\_de\_minimo\_32\_caracteres](#jwt_secret_keyuna_clave_larga_y_segura_de_minimo_32_caracteres)
  - [4. Instalar dependencias](#4-instalar-dependencias)
  - [poetry install](#poetry-install)
  - [5. Levantar la base de datos](#5-levantar-la-base-de-datos)
  - [docker compose up -d db](#docker-compose-up--d-db)
  - [6. Ejecutar migraciones](#6-ejecutar-migraciones)
  - [poetry run alembic upgrade head](#poetry-run-alembic-upgrade-head)
  - [7. Iniciar la aplicación](#7-iniciar-la-aplicación)
  - [http://127.0.0.1:8000](#http1270018000)
  - [Variables de entorno](#variables-de-entorno)
    - [Base de datos y migraciones](#base-de-datos-y-migraciones)
  - [Generar una nueva migración](#generar-una-nueva-migración)
    - [Ejecución de la aplicación](#ejecución-de-la-aplicación)
  - [Ejecución local](#ejecución-local)
  - [poetry run uvicorn orders\_service.main:app --reload](#poetry-run-uvicorn-orders_servicemainapp---reload)
  - [Ejecutar en otro puerto](#ejecutar-en-otro-puerto)
  - [poetry run uvicorn orders\_service.main:app --reload --port 8001](#poetry-run-uvicorn-orders_servicemainapp---reload---port-8001)
  - [Endpoint de salud](#endpoint-de-salud)
  - [curl http://127.0.0.1:8000/health](#curl-http1270018000health)
    - [Documentación de la API](#documentación-de-la-api)
  - [| OpenAPI JSON | `http://127.0.0.1:8000/openapi.json` |](#-openapi-json--http1270018000openapijson-)
  - [Autenticación](#autenticación)
  - [Password: Admin1234!](#password-admin1234)
  - [Obtener un token](#obtener-un-token)
  - [}](#)
  - [Usar el token](#usar-el-token)
  - [Pulsa Authorize.](#pulsa-authorize)
  - [Endpoints](#endpoints)

---

## Características

- Creación de órdenes con uno o varios productos.
- Cálculo automático del total de una orden.
- Consulta de una orden por identificador.
- Listado de órdenes.
- Actualización del estado de una orden.
- Eliminación de órdenes.
- Estados disponibles:
  - `pending`
  - `paid`
  - `cancelled`
- Autenticación mediante JWT.
- Validación de datos de entrada mediante Pydantic.
- Persistencia en PostgreSQL mediante SQLAlchemy.
- Gestión de cambios de base de datos mediante Alembic.
- Pruebas unitarias, de integración y de API.
- Formateo, linting y tipado estático.
- Ejecución local y mediante Docker.
- Pipeline de integración continua con GitHub Actions.
- Auditoría de dependencias con `pip-audit`.

---

## Arquitectura

El proyecto se organiza siguiendo Arquitectura Hexagonal / Limpia.

```text
src/orders_service/
├── domain/
│   ├── entities.py
│   ├── exceptions.py
│   └── repositories.py
│
├── application/
│   ├── dto.py
│   ├── ports.py
│   ├── exceptions.py
│   └── use_cases/
│       ├── create_order.py
│       ├── get_order.py
│       ├── list_orders.py
│       ├── update_order_status.py
│       └── delete_order.py
│
├── infrastructure/
│   ├── db/
│   │   ├── base.py
│   │   ├── models.py
│   │   ├── repositories.py
│   │   └── session.py
│   ├── notifications/
│   │   └── logging_notifier.py
│   └── security/
│       └── jwt.py
│
├── presentation/
│   ├── dependencies.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── health.py
│   │   └── orders.py
│   └── schemas/
│       ├── auth.py
│       └── orders.py
│
├── config.py
└── main.py
```
---

## Diagrama de arquitectura general

flowchart TB
    Client[Cliente / Swagger / Frontend]

    subgraph Presentation["Capa de presentación"]
        API[FastAPI]
        Routers[Routers]
        Schemas[Esquemas Pydantic]
        Dependencies[Dependencias]
    end

    subgraph Application["Capa de aplicación"]
        UseCases[Casos de uso]
        DTOs[DTOs]
        Ports[Puertos / Protocols]
    end

    subgraph Domain["Capa de dominio"]
        Entities[Entidades: Order y OrderItem]
        Rules[Reglas de negocio]
        RepositoryPort[Puerto OrderRepository]
    end

    subgraph Infrastructure["Capa de infraestructura"]
        RepositoryAdapter[Adaptador SQLAlchemy]
        NotifierAdapter[Adaptador de notificación]
        JWT[JWT]
        ORM[Modelos SQLAlchemy]
    end

    DB[(PostgreSQL)]

    Client --> API
    API --> Routers
    Routers --> Schemas
    Routers --> Dependencies
    Routers --> UseCases

    UseCases --> DTOs
    UseCases --> Entities
    UseCases --> Rules
    UseCases --> Ports
    UseCases --> RepositoryPort

    RepositoryAdapter -. implementa .-> RepositoryPort
    NotifierAdapter -. implementa .-> Ports

    UseCases --> RepositoryAdapter
    UseCases --> NotifierAdapter

    API --> JWT
    RepositoryAdapter --> ORM
    ORM --> DB

---

## Diagrama de dependencias por capas
flowchart LR
    Presentation[Presentación<br/>FastAPI, routers, schemas]
    Application[Aplicación<br/>Casos de uso, DTOs, puertos]
    Domain[Dominio<br/>Entidades y reglas]
    Infrastructure[Infraestructura<br/>DB, SQLAlchemy, JWT, logging]

    Presentation --> Application
    Application --> Domain
    Infrastructure --> Application
    Infrastructure --> Domain

---

## Diagrama de flujo para crear una orden
sequenceDiagram
    actor Usuario
    participant API as FastAPI /orders
    participant Auth as Validación JWT
    participant UC as CreateOrderUseCase
    participant Repo as SqlAlchemyOrderRepository
    participant DB as PostgreSQL
    participant Notifier as LoggingOrderNotifier

    Usuario->>API: POST /orders + Bearer Token
    API->>Auth: Validar token JWT
    Auth-->>API: Usuario autenticado
    API->>UC: execute(CreateOrderInput)
    UC->>UC: Crear Order y OrderItem
    UC->>Repo: add(order)
    Repo->>DB: INSERT orders e items
    DB-->>Repo: Orden persistida
    Repo-->>UC: Order guardada
    UC->>Notifier: order_created(order)
    Notifier-->>UC: Registro en logs
    UC-->>API: OrderOutput
    API-->>Usuario: HTTP 201 Created

---

## Diagrama de entidades de base de datos
erDiagram
    ORDERS {
        uuid id PK
        string customer_email
        string status
    }

    ORDER_ITEMS {
        int id PK
        uuid order_id FK
        string product_name
        int quantity
        decimal unit_price
    }

    ORDERS ||--o{ ORDER_ITEMS : contiene
---

## Diagrama de estados de una orden
stateDiagram-v2
    [*] --> pending

    pending --> paid: mark_as_paid
    pending --> cancelled: cancel

    paid --> [*]
    cancelled --> [*]
---

## Tecnologías
| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje principal |
| FastAPI | Framework para API REST |
| Uvicorn | Servidor ASGI |
| Pydantic | Validación y serialización de datos |
| SQLAlchemy | ORM y acceso a datos |
| PostgreSQL | Base de datos relacional |
| Alembic | Migraciones de base de datos |
| Poetry | Gestión de dependencias y entorno |
| PyJWT | Generación y validación de JWT |
| pwdlib | Hashing seguro de contraseñas |
| Pytest | Pruebas automatizadas |
| Ruff | Linter y formateador |
| mypy | Verificación estática de tipos |
| pre-commit | Validaciones antes de cada commit |
| Docker | Contenerización |
| GitHub Actions | Integración continua |
| pip-audit | Auditoría de vulnerabilidades |
---

## Requisitos previos
Python 3.12 o superior.
Poetry.
Docker Desktop.
Git.
Visual Studio Code

Verificación de instalación:
python --version
poetry --version
docker --version
docker compose version
git --version
---

### Instalación y configuración local

## 1. Clonar el repositorio
git clone URL_DEL_REPOSITORIO
cd orders-service

## 2. Crear el archivo de variables de entorno
Copy-Item .env.example .env
---

## 3. Configurar las variables de entorno
Abre el archivo .env y define una clave JWT propia:
JWT_SECRET_KEY=una_clave_larga_y_segura_de_minimo_32_caracteres
---

## 4. Instalar dependencias
poetry install
---

## 5. Levantar la base de datos
docker compose up -d db
---

## 6. Ejecutar migraciones
poetry run alembic upgrade head
---

## 7. Iniciar la aplicación
poetry run uvicorn orders_service.main:app --reload

Aplicación disponible en:
http://127.0.0.1:8000
---

## Variables de entorno
| Variable | Descripción | Ejemplo |
|---|---|---|
| `APP_NAME` | Nombre de la aplicación | `Orders Service` |
| `APP_ENV` | Entorno de ejecución | `development` |
| `DEBUG` | Activa o desactiva modo debug | `true` |
| `DATABASE_URL` | URL de conexión a PostgreSQL | `postgresql+psycopg://orders_user:orders_password@localhost:5432/orders_db` |
| `JWT_SECRET_KEY` | Clave privada para firmar tokens | Texto largo y secreto |
| `JWT_ALGORITHM` | Algoritmo JWT | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token en minutos | `60` |
| `POSTGRES_DB` | Nombre de la base de datos | `orders_db` |
| `POSTGRES_USER` | Usuario de PostgreSQL | `orders_user` |
| `POSTGRES_PASSWORD` | Contraseña de PostgreSQL | `orders_password` |

Ejemplo de .env.example:
APP_NAME=Orders Service
APP_ENV=development
DEBUG=true

DATABASE_URL=postgresql+psycopg://orders_user:orders_password@localhost:5432/orders_db

JWT_SECRET_KEY=replace_this_with_a_long_random_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

POSTGRES_DB=orders_db
POSTGRES_USER=orders_user
POSTGRES_PASSWORD=orders_password

---

### Base de datos y migraciones

## Generar una nueva migración
Después de modificar un modelo de SQLAlchemy:
- poetry run alembic revision --autogenerate -m "descripcion del cambio"
Aplicar migraciones pendientes
- poetry run alembic upgrade head
Consultar versión actual
- poetry run alembic current
Revertir la última migración
- poetry run alembic downgrade -1
---

### Ejecución de la aplicación

## Ejecución local
poetry run uvicorn orders_service.main:app --reload
---

## Ejecutar en otro puerto
poetry run uvicorn orders_service.main:app --reload --port 8001
---

## Endpoint de salud
curl http://127.0.0.1:8000/health
---

### Documentación de la API
FastApi
| Recurso | URL |
|---|---|
| Swagger UI | `http://127.0.0.1:8000/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` |
| OpenAPI JSON | `http://127.0.0.1:8000/openapi.json` |
---

## Autenticación
- Credenciales de demostración
Email: admin@example.com
Password: Admin1234!
---

## Obtener un token
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "Admin1234!"
  }'

Respuesta esperada:
{
  "access_token": "TOKEN_JWT_GENERADO",
  "token_type": "bearer"
}
---

## Usar el token
Authorization: Bearer TOKEN_JWT_GENERADO

En Swagger UI:

Abre http://127.0.0.1:8000/docs.
Ejecuta POST /auth/login.
Copia el valor de access_token.
Pulsa el botón Authorize.
Escribe Bearer seguido del token.
Pulsa Authorize.
---

## Endpoints
| Método | Ruta | Autenticación | Descripción |
|---|---|---:|---|
| `GET` | `/health` | No | Comprueba que la API está disponible |
| `POST` | `/auth/login` | No | Genera un token JWT |
| `POST` | `/orders` | Sí | Crea una orden |
| `GET` | `/orders` | Sí | Lista todas las órdenes |
| `GET` | `/orders/{order_id}` | Sí | Obtiene una orden por ID |
| `PATCH` | `/orders/{order_id}/status` | Sí | Actualiza el estado de una orden |
| `DELETE` | `/orders/{order_id}` | Sí | Elimina una orden |

---
