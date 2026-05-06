"""
nbz_client.py — Экономическое ядро НБЗ
Прямая работа с PostgreSQL через asyncpg
"""
import asyncpg
import logging
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

logger = logging.getLogger("cczmp.nbz")

# Конфигурация
NBZ_DSN = "postgresql://cczmp:securepass@localhost:5432/cczmp_db"

class NBZInsufficientFunds(Exception):
    pass

class NBZAccountFrozen(Exception):
    pass

class NBZCreditDenied(Exception):
    pass

@dataclass
class TransactionResult:
    success: bool
    trans_id: Optional[int] = None
    new_balance_sender: Optional[int] = None
    new_balance_receiver: Optional[int] = None
    error: Optional[str] = None

class NBZClient:
    """Клиент Народного Банка Зоны"""
    
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
    
    # ================================================================
    # БАЛАНС И СЧЕТА
    # ================================================================
    
    async def get_balance(self, iin: str) -> int:
        """Получить баланс основного счёта."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT balance_rub, frozen FROM nbz_accounts WHERE iin = $1", iin
            )
            if not row:
                raise ValueError(f"Счёт ИИН {iin} не найден")
            return row["balance_rub"]
    
    async def get_account_info(self, iin: str) -> dict:
        """Полная информация о счёте."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT a.balance_rub, a.frozen, a.freeze_reason, a.credit_debt,
                       c.name, c.faction, c.is_wanted
                FROM nbz_accounts a
                JOIN nchg_citizen_registry c ON a.iin = c.iin
                WHERE a.iin = $1
            """, iin)
            if not row:
                raise ValueError(f"Счёт ИИН {iin} не найден")
            return dict(row)
    
    # ================================================================
    # ДЕБЕТ / КРЕДИТ / ПЕРЕВОД
    # ================================================================
    
    async def debit_account(self, iin: str, amount: int, reason: str,
                            is_shadow: bool = False) -> TransactionResult:
        """Списание со счёта. Проверяет баланс и заморозку."""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Проверка заморозки
                frozen = await conn.fetchval(
                    "SELECT frozen FROM nbz_accounts WHERE iin = $1 FOR UPDATE", iin
                )
                if frozen:
                    raise NBZAccountFrozen(f"Счёт {iin} заморожен")
                
                # Проверка баланса
                balance = await conn.fetchval(
                    "SELECT balance_rub FROM nbz_accounts WHERE iin = $1", iin
                )
                if balance is None:
                    raise ValueError(f"Счёт {iin} не найден")
                if balance < amount:
                    raise NBZInsufficientFunds(
                        f"Недостаточно средств: {balance} < {amount}"
                    )
                
                # Списание
                new_balance = await conn.fetchval(
                    "UPDATE nbz_accounts SET balance_rub = balance_rub - $1, "
                    "updated_at = NOW() WHERE iin = $2 RETURNING balance_rub",
                    amount, iin
                )
                
                # Запись транзакции
                trans_id = await conn.fetchval("""
                    INSERT INTO nbz_transactions 
                    (sender_iin, receiver_iin, amount_rub, trans_type, is_shadow, initiated_by)
                    VALUES ($1, NULL, $2, $3, $4, $1)
                    RETURNING trans_id
                """, iin, amount, reason, is_shadow)
                
                logger.info(f"Списание {amount} RUB с {iin} ({reason}), транзакция #{trans_id}")
                return TransactionResult(
                    success=True, trans_id=trans_id, new_balance_sender=new_balance
                )
    
    async def credit_account(self, iin: str, amount: int, reason: str) -> TransactionResult:
        """Зачисление на счёт."""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                new_balance = await conn.fetchval(
                    "UPDATE nbz_accounts SET balance_rub = balance_rub + $1, "
                    "updated_at = NOW() WHERE iin = $2 RETURNING balance_rub",
                    amount, iin
                )
                if new_balance is None:
                    raise ValueError(f"Счёт {iin} не найден")
                
                trans_id = await conn.fetchval("""
                    INSERT INTO nbz_transactions
                    (sender_iin, receiver_iin, amount_rub, trans_type, initiated_by)
                    VALUES (NULL, $1, $2, $3, 'SYSTEM')
                    RETURNING trans_id
                """, iin, amount, reason)
                
                return TransactionResult(
                    success=True, trans_id=trans_id, new_balance_receiver=new_balance
                )
    
    async def transfer_funds(self, from_iin: str, to_iin: str, amount: int,
                             reason: str = "transfer") -> TransactionResult:
        """Перевод между счетами."""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Проверка отправителя
                sender = await conn.fetchrow(
                    "SELECT balance_rub, frozen FROM nbz_accounts WHERE iin = $1 FOR UPDATE",
                    from_iin
                )
                if not sender:
                    raise ValueError(f"Счёт отправителя {from_iin} не найден")
                if sender["frozen"]:
                    raise NBZAccountFrozen(f"Счёт {from_iin} заморожен")
                if sender["balance_rub"] < amount:
                    raise NBZInsufficientFunds(
                        f"Недостаточно средств: {sender['balance_rub']} < {amount}"
                    )
                
                # Получатель
                receiver = await conn.fetchrow(
                    "SELECT iin FROM nbz_accounts WHERE iin = $1 FOR UPDATE", to_iin
                )
                if not receiver:
                    raise ValueError(f"Счёт получателя {to_iin} не найден")
                
                # Перевод
                new_sender_bal = await conn.fetchval(
                    "UPDATE nbz_accounts SET balance_rub = balance_rub - $1 "
                    "WHERE iin = $2 RETURNING balance_rub",
                    amount, from_iin
                )
                new_receiver_bal = await conn.fetchval(
                    "UPDATE nbz_accounts SET balance_rub = balance_rub + $1 "
                    "WHERE iin = $2 RETURNING balance_rub",
                    amount, to_iin
                )
                
                trans_id = await conn.fetchval("""
                    INSERT INTO nbz_transactions
                    (sender_iin, receiver_iin, amount_rub, trans_type, initiated_by)
                    VALUES ($1, $2, $3, $4, $1)
                    RETURNING trans_id
                """, from_iin, to_iin, amount, reason)
                
                logger.info(f"Перевод {amount} RUB: {from_iin} -> {to_iin} (#{trans_id})")
                return TransactionResult(
                    success=True, trans_id=trans_id,
                    new_balance_sender=new_sender_bal,
                    new_balance_receiver=new_receiver_bal
                )
    
    # ================================================================
    # ТЕНЕВЫЕ КОШЕЛЬКИ (SHADOW WALLET)
    # ================================================================
    
    async def get_shadow_balance(self, iin: str) -> dict:
        """Баланс теневого кошелька."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT balance_rub, total_stolen, laundering_pending "
                "FROM shadow_accounts WHERE iin = $1", iin
            )
            if not row:
                # Автосоздание при первом обращении
                await conn.execute(
                    "INSERT INTO shadow_accounts (iin) VALUES ($1) ON CONFLICT DO NOTHING", iin
                )
                return {"balance_rub": 0, "total_stolen": 0, "laundering_pending": 0}
            return {
                "balance_rub": row["balance_rub"],
                "total_stolen": row["total_stolen"],
                "laundering_pending": row["laundering_pending"]
            }
    
    async def drain_to_shadow(self, attacker_iin: str, target_iin: str,
                              amount: int) -> TransactionResult:
        """Слив средств жертвы в теневой кошелёк атакующего."""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Списание с жертвы
                victim_balance = await conn.fetchval(
                    "SELECT balance_rub FROM nbz_accounts WHERE iin = $1 FOR UPDATE",
                    target_iin
                )
                if victim_balance is None:
                    return TransactionResult(success=False, error="Счёт жертвы не найден")
                if victim_balance < amount:
                    amount = victim_balance  # сливаем всё что есть
                
                await conn.execute(
                    "UPDATE nbz_accounts SET balance_rub = balance_rub - $1 WHERE iin = $2",
                    amount, target_iin
                )
                
                # Зачисление в теневой кошелёк атакующего
                await conn.execute("""
                    INSERT INTO shadow_accounts (iin, balance_rub, total_stolen)
                    VALUES ($1, $2, $2)
                    ON CONFLICT (iin) DO UPDATE
                    SET balance_rub = shadow_accounts.balance_rub + $2,
                        total_stolen = shadow_accounts.total_stolen + $2
                """, attacker_iin, amount)
                
                # Запись транзакции
                trans_id = await conn.fetchval("""
                    INSERT INTO nbz_transactions
                    (sender_iin, receiver_iin, amount_rub, trans_type, is_shadow, initiated_by)
                    VALUES ($1, $2, $3, 'exploit_drain', TRUE, $2)
                    RETURNING trans_id
                """, target_iin, attacker_iin, amount)
                
                logger.info(f"Слив {amount} RUB: {target_iin} -> shadow:{attacker_iin}")
                return TransactionResult(success=True, trans_id=trans_id)
    
    async def launder_funds(self, iin: str, amount: int) -> TransactionResult:
        """
        Отмывка теневых средств с комиссией 30%.
        Деньги переводятся из shadow_accounts в основной nbz_accounts.
        """
        commission = int(amount * 0.30)
        clean_amount = amount - commission
        
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                shadow = await conn.fetchrow(
                    "SELECT balance_rub FROM shadow_accounts WHERE iin = $1 FOR UPDATE", iin
                )
                if not shadow or shadow["balance_rub"] < amount:
                    return TransactionResult(success=False, error="Недостаточно теневых средств")
                
                # Списание из теневого кошелька
                await conn.execute(
                    "UPDATE shadow_accounts SET balance_rub = balance_rub - $1, "
                    "laundering_pending = laundering_pending - $2 WHERE iin = $3",
                    amount, amount, iin
                )
                
                # Зачисление чистой суммы на основной счёт
                await conn.execute(
                    "UPDATE nbz_accounts SET balance_rub = balance_rub + $1 WHERE iin = $2",
                    clean_amount, iin
                )
                
                # Запись транзакции
                trans_id = await conn.fetchval("""
                    INSERT INTO nbz_transactions
                    (sender_iin, receiver_iin, amount_rub, trans_type, is_shadow, initiated_by)
                    VALUES ($1, $1, $2, 'laundering', FALSE, $1)
                    RETURNING trans_id
                """, iin, clean_amount)
                
                logger.info(f"Отмывка {amount} RUB (чистыми {clean_amount}) для {iin}")
                return TransactionResult(
                    success=True, trans_id=trans_id,
                    new_balance_receiver=await conn.fetchval(
                        "SELECT balance_rub FROM nbz_accounts WHERE iin = $1", iin
                    )
                )
    
    # ================================================================
    # КРЕДИТЫ
    # ================================================================
    
    CREDIT_PRODUCTS = {
        "start":    {"amount": 50_000,   "hours": 2,     "rate": 1.2,  "max_per_player": 1},
        "business": {"amount": 250_000,  "hours": 120,   "rate": 0.9,  "max_per_player": 3},
        "wheels":   {"amount": 500_000,  "hours": 240,   "rate": 0.65, "max_per_player": 2},
        "prestige": {"amount": 1_000_000,"hours": 360,   "rate": 0.5,  "max_per_player": 1},
        "dark":     {"amount": 2_000_000,"hours": 72,    "rate": 0.3,  "max_per_player": 1},
    }
    
    async def issue_credit(self, iin: str, credit_type: str) -> TransactionResult:
        """Выдача кредита."""
        if credit_type not in self.CREDIT_PRODUCTS:
            return TransactionResult(success=False, error="Неизвестный тип кредита")
        
        product = self.CREDIT_PRODUCTS[credit_type]
        
        async with self.pool.acquire() as conn:
            # Проверка лимита кредитов этого типа
            active_count = await conn.fetchval(
                "SELECT COUNT(*) FROM nbz_credits WHERE iin = $1 AND credit_type = $2 AND status = 'active'",
                iin, credit_type
            )
            if active_count >= product["max_per_player"]:
                return TransactionResult(success=False, error="Лимит кредитов этого типа исчерпан")
            
            async with conn.transaction():
                # Зачисление на счёт
                await conn.execute(
                    "UPDATE nbz_accounts SET balance_rub = balance_rub + $1 WHERE iin = $2",
                    product["amount"], iin
                )
                
                # Запись кредита
                due_by = f"NOW() + INTERVAL '{product['hours']} hours'"
                credit_id = await conn.fetchval(f"""
                    INSERT INTO nbz_credits (iin, credit_type, amount_rub, remaining_debt, interest_rate, due_by)
                    VALUES ($1, $2, $3, $3, $4, {due_by})
                    RETURNING credit_id
                """, iin, credit_type, product["amount"], product["rate"])
                
                return TransactionResult(success=True, trans_id=credit_id)
    
    # ================================================================
    # БЕЗОПАСНОСТЬ
    # ================================================================
    
    async def freeze_account(self, iin: str, reason: str, admin_iin: str) -> bool:
        """Заморозка счёта (для СЧЁС/МВД)."""
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "UPDATE nbz_accounts SET frozen = TRUE, freeze_reason = $1 WHERE iin = $2",
                f"{reason} (инициатор: {admin_iin})", iin
            )
            logger.warning(f"Счёт {iin} заморожен: {reason}")
            return result != "UPDATE 0"
    
    async def unfreeze_account(self, iin: str) -> bool:
        """Разморозка счёта."""
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "UPDATE nbz_accounts SET frozen = FALSE, freeze_reason = NULL WHERE iin = $1", iin
            )
            return result != "UPDATE 0"