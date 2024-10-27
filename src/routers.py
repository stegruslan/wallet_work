from fastapi import APIRouter

from schemas import WalletResponse, WalletBalance
from services import create_wallet, process_operation, get_balance_wallet

# Роутер для управления кошельками с префиксом '/wallets'
router = APIRouter(prefix="/wallets", tags=["wallets"])

router.post("/", response_model=WalletResponse)(create_wallet)

router.post("/{wallet_id}/operation", response_model=WalletResponse)(process_operation)

router.get("/{wallet_id}/", response_model=WalletBalance)(get_balance_wallet)
