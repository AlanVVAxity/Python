from fastapi import FastAPI

from modulo_08.infrastructure.config import get_settings
from modulo_08.presentation.routers.orders import router as orders_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.include_router(orders_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.app_env,
    }
