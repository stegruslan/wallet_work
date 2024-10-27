from decimal import Decimal
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_wallet():
    """
    Тест на создание нового кошелька.
    Проверяет, что при создании кошелька сервер возвращает статус 200 и
    содержит поле 'id' в ответе.

    """
    response = client.post("/api/v1/wallets/")
    assert response.status_code == 200
    assert "id" in response.json()


def test_process_operation():
    """
    Тест на обработку операции с кошельком.
    1. Создает новый кошелек и получает его ID.
    2. Получает начальный баланс кошелька.
    3. Выполняет операцию депозита на сумму 100.
    4. Проверяет, что статус ответа 200 и баланс обновился правильно.

    """

    # Создаем кошелек и получаем его ID
    wallet_id = client.post("/api/v1/wallets/").json()["id"]

    # Получаем начальный баланс
    initial_balance = Decimal(client.get(f"/api/v1/wallets/{wallet_id}/").json()["balance"])

    # Выполняем операцию депозита
    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json={"operationType": "DEPOSIT", "amount": 100})
    assert response.status_code == 200

    # Проверяем, что баланс обновился
    updated_balance = Decimal(response.json()["balance"])
    assert updated_balance == (initial_balance + Decimal(100))


def test_get_balance_wallet():
    """
    Тест на получение баланса кошелька.
    Проверяет, что при запросе баланса кошелька сервер возвращает статус 200
    и содержит поле 'balance' в ответе.

    """
    response = client.get("/api/v1/wallets/9c20b3ac-91b0-4c7c-8296-1eea1ac16eef/")
    assert response.status_code == 200
    assert "balance" in response.json()
