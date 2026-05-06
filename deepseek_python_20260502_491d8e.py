"""
cczmp_pda_handlers.py
Серверные обработчики событий КПК с интеграцией NBZ и СЧЁС
Архитектура: JSON-RPC поверх TCP, асинхронный I/O
"""
import logging
import math
import time
import json
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from nbz_client import NBZClient, NBZInsufficientFunds, NBZAccountFrozen

logger = logging.getLogger("cczmp.handlers.pda")

# ============================================================
# КОНСТАНТЫ
# ============================================================

MAX_SMS_DISTANCE = 500      # метров
MAX_CALL_DISTANCE = 500     # метров
SMS_COST_PER_BYTE = 10      # RUB
CALL_COST_PER_SEC = 10      # RUB
CALL_MIN_COST = 50          # RUB
DETECTION_BASE_CHANCE = 0.10
DETECTION_FW_MULTIPLIER = 0.008
DETECTION_MAX_CHANCE = 0.95

# Активные брутфорс-сессии (в продакшене — Redis, здесь — in-memory)
_active_exploit_sessions: Dict[str, Dict[str, Any]] = {}


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def calculate_distance(pos1: tuple, pos2: tuple) -> float:
    """
    Расчёт евклидова расстояния между двумя точками в игровом мире.
    pos = (x, y, z) в метрах.
    В реальной реализации берётся из данных сервера об игроках.
    Здесь — заглушка, показывающая принцип.
    """
    if not pos1 or not pos2:
        return 0.0
    return math.sqrt(
        (pos1[0] - pos2[0])**2 + 
        (pos1[1] - pos2[1])**2 + 
        (pos1[2] - pos2[2])**2
    )


def get_player_position(uid: int) -> Optional[tuple]:
    """
    Получение позиции игрока из кэша/БД сервера.
    Заглушка — в реальности запрос к серверному кэшу позиций.
    """
    # TODO: заменить на реальный запрос к player_position_cache
    player_cache = {
        # uid: (x, y, z)
    }
    return player_cache.get(uid)


def get_player_iin(uid: int) -> Optional[str]:
    """
    Получение ИИН по UID игрока.
    Заглушка — в реальности запрос к БД или кэшу.
    """
    # TODO: запрос к nchg_citizen_registry по UID персонажа
    return None


def get_player_firewall(uid: int) -> int:
    """
    Получение текущего Firewall игрока по его активному устройству.
    Заглушка.
    """
    # TODO: запрос к инвентарю/экипировке игрока
    return 10  # дефолт для бюджетного КПК


def get_player_device_type(uid: int) -> str:
    """Тип устройства игрока."""
    # TODO: запрос к активному предмету КПК
    return "pda_budget"


# ============================================================
# ОБРАБОТЧИК: PDA_SMS_SEND
# Событие: pda_sms_send
# ============================================================

async def handle_pda_sms_send(nbz: NBZClient, payload: dict, 
                              player_positions: dict) -> dict:
    """
    Обработка отправки SMS.
    
    payload:
        sender_uid: int      — UID отправителя
        target_uid: int      — UID получателя
        text: str            — текст сообщения
        byte_count: int      — размер в байтах
        tariff: int          — стоимость за байт (клиент передаёт для проверки)
        msg_id: str          — клиентский ID сообщения
    
    Возвращает:
        { ok: bool, err: Optional[str], cost: int }
    """
    sender_uid = payload.get("sender_uid")
    target_uid = payload.get("target_uid")
    text = payload.get("text", "")
    byte_count = payload.get("byte_count", len(text))
    tariff = payload.get("tariff", SMS_COST_PER_BYTE)
    msg_id = payload.get("msg_id", "unknown")

    # === Валидация ===
    if not sender_uid or not target_uid:
        return {"ok": False, "err": "Неверные UID отправителя или получателя", "cost": 0}
    
    if sender_uid == target_uid:
        return {"ok": False, "err": "Нельзя отправить SMS самому себе", "cost": 0}
    
    if not text or byte_count == 0:
        return {"ok": False, "err": "Пустое сообщение", "cost": 0}

    # === Проверка дистанции ===
    sender_pos = player_positions.get(sender_uid)
    target_pos = player_positions.get(target_uid)
    
    if not sender_pos or not target_pos:
        return {"ok": False, "err": "Не удалось определить позицию игрока", "cost": 0}
    
    distance = calculate_distance(sender_pos, target_pos)
    
    if distance > MAX_SMS_DISTANCE:
        logger.info(f"SMS отклонена: дистанция {distance:.0f}м > {MAX_SMS_DISTANCE}м")
        return {
            "ok": False, 
            "err": f"Абонент вне зоны действия сети ({distance:.0f}м > {MAX_SMS_DISTANCE}м)", 
            "cost": 0
        }

    # === Расчёт стоимости ===
    cost = byte_count * tariff
    sender_iin = get_player_iin(sender_uid)
    target_iin = get_player_iin(target_uid)
    
    if not sender_iin:
        return {"ok": False, "err": "Отправитель не найден в реестре граждан", "cost": 0}

    # === Списание средств через НБЗ ===
    try:
        result = await nbz.debit_account(
            iin=sender_iin,
            amount=cost,
            reason=f"sms_to_{target_uid}",
            is_shadow=False
        )
        
        if not result.success:
            return {"ok": False, "err": result.error or "Ошибка списания", "cost": 0}
        
        logger.info(f"SMS доставлена: UID:{sender_uid} -> UID:{target_uid}, "
                    f"{byte_count} байт, {cost} RUB, dist={distance:.0f}м")
        
        return {
            "ok": True,
            "err": None,
            "cost": cost,
            "trans_id": result.trans_id,
            "msg_id": msg_id,
            "new_balance": result.new_balance_sender
        }
    
    except NBZInsufficientFunds:
        return {"ok": False, "err": "Недостаточно средств на счету НБЗ", "cost": 0}
    except NBZAccountFrozen:
        return {"ok": False, "err": "Ваш счёт заморожен", "cost": 0}
    except Exception as e:
        logger.error(f"Ошибка при отправке SMS: {e}")
        return {"ok": False, "err": "Внутренняя ошибка банковской системы", "cost": 0}


# ============================================================
# ОБРАБОТЧИК: PDA_NMAP_SCAN
# Событие: pda_nmap_scan
# ============================================================

async def handle_pda_nmap_scan(nbz: NBZClient, payload: dict,
                               player_positions: dict) -> dict:
    """
    Обработка сканирования ближних КПК через nmap.
    
    payload:
        sender_uid: int      — UID сканирующего
        range: int           — дальность сканирования (из конфига устройства)
    
    Возвращает:
        {
            targets: [
                { uid, iin, distance, firewall, device_type },
                ...
            ],
            range: int,
            scan_time: str
        }
    """
    sender_uid = payload.get("sender_uid")
    scan_range = payload.get("range", 500)
    scan_range = min(scan_range, 800)  # аппаратное ограничение
    
    if not sender_uid:
        return {"targets": [], "error": "Неверный UID сканирующего"}
    
    sender_pos = player_positions.get(sender_uid)
    if not sender_pos:
        return {"targets": [], "error": "Не удалось определить позицию"}
    
    sender_iin = get_player_iin(sender_uid)
    
    # === Поиск целей в радиусе ===
    targets = []
    
    for uid, pos in player_positions.items():
        if uid == sender_uid:
            continue
        
        distance = calculate_distance(sender_pos, pos)
        if distance > scan_range:
            continue
        
        iin = get_player_iin(uid)
        firewall = get_player_firewall(uid)
        device_type = get_player_device_type(uid)
        
        # Скрываем ИИН если у сканирующего нет прав СЧЁС
        # (проверка по фракции/допуску)
        visible_iin = iin  # TODO: добавить проверку прав доступа
        
        targets.append({
            "uid": uid,
            "iin": visible_iin,
            "distance": round(distance, 1),
            "firewall": firewall,
            "device_type": device_type
        })
    
    # Сортировка по расстоянию
    targets.sort(key=lambda t: t["distance"])
    
    # === Логирование в СЧЁС ===
    # nmap сам по себе не является атакой, но фиксируется для статистики
    if sender_iin:
        for target in targets:
            await _log_security_event(
                nbz=nbz,
                attacker_iin=sender_iin,
                target_iin=target["iin"],
                event_type="nmap_scan",
                exploit_used=None,
                detection_chance=0.0,
                was_detected=False,
                payload_extra={
                    "scan_range": scan_range,
                    "target_firewall": target["firewall"],
                    "distance": target["distance"]
                }
            )
    
    logger.info(f"nmap: UID:{sender_uid} просканировал {len(targets)} целей в радиусе {scan_range}м")
    
    return {
        "targets": targets,
        "range": scan_range,
        "scan_time": time.strftime("%H:%M:%S")
    }


# ============================================================
# ОБРАБОТЧИК: PDA_EXPLOIT_START
# Событие: pda_exploit_start
# ============================================================

async def handle_pda_exploit_start(nbz: NBZClient, payload: dict,
                                   player_positions: dict) -> dict:
    """
    Запуск брутфорс-атаки на КПК цели.
    
    payload:
        sender_uid: int      — UID атакующего
        target_uid: int      — UID цели
        exploit_type: str    — тип эксплойта (freeze_pda, drain_wallet, block_sms, spoof_id)
        target_fw: int       — Firewall цели (клиентская оценка)
        crack_time: float    — расчётное время взлома (клиентская оценка)
    
    Возвращает:
        {
            ok: bool,
            err: Optional[str],
            session_id: str,
            estimated_time: float,
            detected: bool
        }
    """
    sender_uid = payload.get("sender_uid")
    target_uid = payload.get("target_uid")
    exploit_type = payload.get("exploit_type", "freeze_pda")
    client_target_fw = payload.get("target_fw", 50)
    client_crack_time = payload.get("crack_time", 10.0)
    
    # === Валидация ===
    if not sender_uid or not target_uid:
        return {"ok": False, "err": "Неверные UID"}
    
    if sender_uid == target_uid:
        return {"ok": False, "err": "Нельзя атаковать самого себя"}
    
    sender_iin = get_player_iin(sender_uid)
    target_iin = get_player_iin(target_uid)
    
    if not sender_iin or not target_iin:
        return {"ok": False, "err": "Участники не найдены в реестре"}
    
    # === Реальный Firewall цели (серверная проверка) ===
    real_target_fw = get_player_firewall(target_uid)
    
    # === Расчёт реального времени взлома ===
    EXPLOIT_CONFIG = {
        "freeze_pda":   {"base_time": 8,  "fw_mod": 0.15, "drain_pct": 0},
        "drain_wallet": {"base_time": 12, "fw_mod": 0.20, "drain_pct": 0.12, "max_drain": 5000},
        "block_sms":    {"base_time": 5,  "fw_mod": 0.10, "drain_pct": 0},
        "spoof_id":     {"base_time": 20, "fw_mod": 0.30, "drain_pct": 0},
    }
    
    expl_cfg = EXPLOIT_CONFIG.get(exploit_type)
    if not expl_cfg:
        return {"ok": False, "err": f"Неизвестный тип эксплойта: {exploit_type}"}
    
    real_crack_time = expl_cfg["base_time"] + (real_target_fw * expl_cfg["fw_mod"])
    
    # === Расчёт шанса обнаружения ===
    detection_chance = min(
        DETECTION_BASE_CHANCE + (real_target_fw * DETECTION_FW_MULTIPLIER),
        DETECTION_MAX_CHANCE
    )
    
    import random
    was_detected = random.random() < detection_chance
    
    # === Создание сессии взлома ===
    session_id = f"exploit_{sender_uid}_{target_uid}_{int(time.time())}"
    
    _active_exploit_sessions[session_id] = {
        "attacker_uid": sender_uid,
        "attacker_iin": sender_iin,
        "target_uid": target_uid,
        "target_iin": target_iin,
        "exploit_type": exploit_type,
        "target_fw": real_target_fw,
        "crack_time": real_crack_time,
        "started_at": time.time(),
        "detection_chance": detection_chance,
        "was_detected": was_detected,
        "drain_pct": expl_cfg.get("drain_pct", 0),
        "max_drain": expl_cfg.get("max_drain", 0),
        "status": "cracking"
    }
    
    # === Логирование в СЧЁС ===
    await _log_security_event(
        nbz=nbz,
        attacker_iin=sender_iin,
        target_iin=target_iin,
        event_type="exploit_attempt",
        exploit_used=exploit_type,
        detection_chance=detection_chance,
        was_detected=was_detected,
        payload_extra={
            "session_id": session_id,
            "target_fw": real_target_fw,
            "crack_time": real_crack_time
        }
    )
    
    if was_detected:
        # Установка флага наблюдения на атакующего
        await _set_monitoring_flag(nbz, sender_iin, 
                                   f"Обнаружена попытка взлома [{exploit_type}] цели {target_iin}")
    
    logger.info(
        f"msf: {exploit_type} UID:{sender_uid}->UID:{target_uid} "
        f"session={session_id} fw={real_target_fw} t={real_crack_time:.1f}s "
        f"detect={'YES' if was_detected else 'no'}"
    )
    
    return {
        "ok": True,
        "err": None,
        "session_id": session_id,
        "estimated_time": round(real_crack_time, 1),
        "real_fw": real_target_fw,
        "detected": was_detected
    }


# ============================================================
# ОБРАБОТЧИК: PDA_EXPLOIT_COMPLETE
# Вызывается по завершении таймера на сервере
# ============================================================

async def handle_pda_exploit_complete(nbz: NBZClient, session_id: str) -> dict:
    """
    Завершение брутфорс-сессии. Выполняет реальный эффект эксплойта.
    """
    session = _active_exploit_sessions.pop(session_id, None)
    if not session:
        return {"ok": False, "err": "Сессия не найдена"}
    
    attacker_iin = session["attacker_iin"]
    target_iin = session["target_iin"]
    exploit_type = session["exploit_type"]
    drain_pct = session["drain_pct"]
    max_drain = session["max_drain"]
    
    drained = 0
    shadow_balance = 0
    
    try:
        if exploit_type == "drain_wallet":
            # Получаем баланс жертвы
            target_balance = await nbz.get_balance(target_iin)
            drain_amount = min(int(target_balance * drain_pct), max_drain)
            
            if drain_amount > 0:
                # Сливаем в теневой кошелёк атакующего
                result = await nbz.drain_to_shadow(
                    attacker_iin=attacker_iin,
                    target_iin=target_iin,
                    amount=drain_amount
                )
                if result.success:
                    drained = drain_amount
                    
                    # Логируем успешную кражу в СЧЁС
                    await _log_security_event(
                        nbz=nbz,
                        attacker_iin=attacker_iin,
                        target_iin=target_iin,
                        event_type="exploit_success",
                        exploit_used="drain_wallet",
                        detection_chance=session["detection_chance"],
                        was_detected=session["was_detected"],
                        payload_extra={
                            "drained_rub": drained,
                            "session_id": session_id
                        }
                    )
        
        elif exploit_type == "freeze_pda":
            # Отправляем target_uid ивент о заморозке КПК на 30 секунд
            # В реальности — через event bus к клиенту цели
            pass
        
        elif exploit_type == "block_sms":
            # Блокировка SMS на 60 секунд
            pass
        
        elif exploit_type == "spoof_id":
            # Спуфинг ИИН на 120 секунд
            pass
        
        # Получаем теневой баланс после операции
        shadow = await nbz.get_shadow_balance(attacker_iin)
        shadow_balance = shadow["balance_rub"]
        
        logger.info(f"msf complete: {exploit_type} session={session_id} drained={drained}")
        
        return {
            "ok": True,
            "drained": drained,
            "shadow_balance": shadow_balance,
            "detected": session["was_detected"],
            "target_fw": session["target_fw"]
        }
    
    except Exception as e:
        logger.error(f"Ошибка при завершении эксплойта {session_id}: {e}")
        return {"ok": False, "err": str(e)}


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ БЕЗОПАСНОСТИ
# ============================================================

async def _log_security_event(
    nbz: NBZClient,
    attacker_iin: Optional[str],
    target_iin: str,
    event_type: str,
    exploit_used: Optional[str],
    detection_chance: float,
    was_detected: bool,
    payload_extra: Optional[dict] = None
):
    """
    Запись события в журнал безопасности СЧЁС.
    Использует прямой доступ к пулу БД через nbz.pool.
    """
    try:
        async with nbz.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO schs_security_log
                (attacker_iin, target_iin, event_type, exploit_used,
                 detection_chance, was_detected, payload_json)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, 
                attacker_iin,
                target_iin,
                event_type,
                exploit_used,
                detection_chance,
                was_detected,
                json.dumps(payload_extra or {})
            )
    except Exception as e:
        logger.error(f"Ошибка записи в security_log: {e}")


async def _set_monitoring_flag(nbz: NBZClient, iin: str, reason: str):
    """
    Установка флага наблюдения СЧЁС на гражданина.
    """
    try:
        async with nbz.pool.acquire() as conn:
            # Проверяем, нет ли уже активного флага
            existing = await conn.fetchval(
                "SELECT COUNT(*) FROM schs_monitoring_flags WHERE iin = $1 AND is_active = TRUE",
                iin
            )
            if existing == 0:
                await conn.execute("""
                    INSERT INTO schs_monitoring_flags (iin, reason, set_by)
                    VALUES ($1, $2, 'SYSTEM_AUTO')
                """, iin, reason)
                
                # Обновляем флаг в реестре граждан
                await conn.execute(
                    "UPDATE nchg_citizen_registry SET is_monitored = TRUE WHERE iin = $1",
                    iin
                )
                logger.info(f"Установлен флаг наблюдения для {iin}: {reason}")
    except Exception as e:
        logger.error(f"Ошибка установки флага наблюдения: {e}")


# ============================================================
# РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ В CCZMP EVENT BUS
# ============================================================

def register_handlers(event_bus, nbz_pool):
    """
    Регистрация всех PDA-обработчиков в шине событий CCZMP.
    Вызывается при старте сервера.
    
    event_bus: объект шины событий с методом on(event_name, handler)
    nbz_pool: пул подключений asyncpg
    """
    nbz = NBZClient(nbz_pool)
    
    # Кэш позиций игроков (в реальности — singleton или Redis)
    player_positions: Dict[int, tuple] = {}
    
    # Функция обновления позиций (вызывается из игрового цикла сервера)
    def update_player_positions(positions: dict):
        player_positions.clear()
        player_positions.update(positions)
    
    @event_bus.on("pda_sms_send")
    async def on_sms_send(payload):
        return await handle_pda_sms_send(nbz, payload, player_positions)
    
    @event_bus.on("pda_nmap_scan")
    async def on_nmap_scan(payload):
        return await handle_pda_nmap_scan(nbz, payload, player_positions)
    
    @event_bus.on("pda_exploit_start")
    async def on_exploit_start(payload):
        return await handle_pda_exploit_start(nbz, payload, player_positions)
    
    @event_bus.on("pda_exploit_complete")
    async def on_exploit_complete(payload):
        session_id = payload.get("session_id")
        return await handle_pda_exploit_complete(nbz, session_id)
    
    logger.info("PDA-обработчики зарегистрированы в CCZMP Event Bus")
    
    return {
        "update_positions": update_player_positions,
        "nbz": nbz
    }