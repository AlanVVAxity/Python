"""Clase base y mixins compartidos por los modelos."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Clase base declarativa de todos los modelos del módulo."""


class TimestampMixin:
    """Agrega la fecha de creación gestionada por la base de datos."""

    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
