from fastapi import FastAPI

from orders_service.config import get_settings
from orders_service.presentation.routers import auth, health, orders

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(orders.router)
