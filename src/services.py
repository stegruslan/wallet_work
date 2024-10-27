import uuid
from datetime import datetime

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database import session_factory
from models import Wallets
from schemas import WalletResponse, OperationRequest, WalletBalance


def create_wallet() -> WalletResponse:
    """
        Создает новый кошелек с начальным балансом 0.

        Returns:
            WalletResponse: Информация о созданном кошельке, включая его уникальный идентификатор,
                            баланс, дату и время создания и последнего обновления.
        """
    with session_factory() as session:
        new_wallet = Wallets(
            id=uuid.uuid4(),
            balance=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        session.add(new_wallet)
        session.commit()
        return WalletResponse(
            id=new_wallet.id,
            balance=new_wallet.balance,
            created_at=new_wallet.created_at,
            updated_at=new_wallet.updated_at, )


def process_operation(wallet_id: uuid.UUID, operation: OperationRequest) -> WalletResponse:
    """
        Обрабатывает операцию (пополнение или снятие средств) для указанного кошелька.

        Args:
            wallet_id (uuid.UUID): Уникальный идентификатор кошелька.
            operation (OperationRequest): Запрос на операцию с указанием типа и суммы.

        Returns:
            WalletResponse: Обновленная информация о кошельке после операции.

        Raises:
            HTTPException: Если кошелек не найден (404) или недостаточно средств для снятия (400).
        """
    with session_factory() as session:
        wallet = session.query(Wallets).filter(Wallets.id == wallet_id).with_for_update().first()
        if wallet is None:
            raise HTTPException(status_code=404, detail="Кошелек не найден")

        if operation.operationType == "DEPOSIT":
            wallet.balance += operation.amount
        elif operation.operationType == "WITHDRAW":
            if wallet.balance < operation.amount:
                raise HTTPException(status_code=400, detail={"Ошибка!": "Недостаточно средств",
                                                             "Текущий баланс": str(wallet.balance),
                                                             "Запрошено на снятие": str(operation.amount)})
            wallet.balance -= operation.amount
        session.commit()
        return WalletResponse(
            id=wallet.id,
            balance=wallet.balance,
            created_at=wallet.created_at,
            updated_at=wallet.updated_at,
        )


def get_balance_wallet(wallet_id: uuid.UUID) -> WalletBalance:
    """
       Получает текущий баланс указанного кошелька.

       Args:
           wallet_id (uuid.UUID): Уникальный идентификатор кошелька.

       Returns:
           WalletBalance: Текущий баланс кошелька.

       Raises:
           HTTPException: Если кошелек не найден (404).
       """
    with session_factory() as session:
        wallet = session.query(Wallets).filter(Wallets.id == wallet_id).first()
        if wallet is None:
            raise HTTPException(status_code=404, detail="Кошелек не найден")
    return WalletBalance(
        balance=wallet.balance,
    )
