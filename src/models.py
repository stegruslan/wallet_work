"""Файл моделей ORM."""
from sqlalchemy import Column, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import declarative_base

# Создаем базовый класс для декларативного стиля
Base = declarative_base()


class Wallets(Base):

    __tablename__ = 'wallets'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, unique=True)
    balance = Column(Numeric(precision=10, scale=2), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


