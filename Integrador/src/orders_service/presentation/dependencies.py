from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from orders_service.infrastructure.db.repositories import SqlAlchemyOrderRepository
from orders_service.infrastructure.db.session import get_db_session
from orders_service.infrastructure.notifications.logging_notifier import (
    LoggingOrderNotifier,
)
from orders_service.infrastructure.security.jwt import decode_access_token

security_scheme = HTTPBearer()


def get_order_repository(
    session: Session = Depends(get_db_session),
) -> SqlAlchemyOrderRepository:
    return SqlAlchemyOrderRepository(session)


def get_order_notifier() -> LoggingOrderNotifier:
    return LoggingOrderNotifier()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> str:
    try:
        return decode_access_token(credentials.credentials)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
