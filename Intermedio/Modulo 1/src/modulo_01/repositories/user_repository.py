"""Operaciones de persistencia sobre usuarios."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from modulo_01.models import User


class UserRepository:
    """CRUD de usuarios sobre una sesión de SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def crear(self, *, email: str, nombre: str) -> User:
        user = User(email=email, nombre=nombre)
        self._session.add(user)
        self._session.flush()
        return user

    def obtener(self, user_id: int) -> User | None:
        return self._session.get(User, user_id)

    def buscar_por_email(self, email: str) -> User | None:
        return self._session.scalar(select(User).where(User.email == email))

    def listar(self, *, solo_activos: bool = False) -> list[User]:
        stmt = select(User).order_by(User.id)
        if solo_activos:
            stmt = stmt.where(User.activo.is_(True))
        return list(self._session.scalars(stmt))

    def desactivar(self, user_id: int) -> User | None:
        user = self.obtener(user_id)
        if user is None:
            return None
        user.activo = False
        self._session.flush()
        return user

    def eliminar(self, user_id: int) -> bool:
        user = self.obtener(user_id)
        if user is None:
            return False
        self._session.delete(user)
        self._session.flush()
        return True
