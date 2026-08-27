from fastapi import FastAPI

from modulo_02.api.routes.health import router as health_router
from modulo_02.api.routes.orders import router as orders_router

app = FastAPI(
    title="Orders API",
    description="API para la gestión de órdenes.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(orders_router)
