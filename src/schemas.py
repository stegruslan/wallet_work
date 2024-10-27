"""Схемы pydantic для работы представлений."""
from enum import Enum

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class WalletResponse(BaseModel):
    """
        Схема ответа для операций с кошельком.
    """
    id: UUID
    balance: Decimal
    created_at: datetime
    updated_at: datetime


class WalletBalance(BaseModel):
    """
        Схема для представления текущего баланса кошелька..
    """
    balance: Decimal


class OperationType(str, Enum):
    """
       Перечисление для типов операций с кошельком.
    """
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class OperationRequest(BaseModel):
    """
        Схема запроса для операций с кошельком.
    """
    operationType: OperationType
    amount: Decimal

    class Config:
        orm_mode = True
