-- ============================================================
-- CCZMP CORE SCHEMA
-- Target: PostgreSQL 15+
-- Normalization: 3NF
-- ============================================================

-- === ГРАЖДАНЕ И ИДЕНТИФИКАЦИЯ ===

CREATE TABLE nchg_citizen_registry (
    iin             CHAR(10)        PRIMARY KEY,  -- 10-значный ИИН
    name            VARCHAR(128)    NOT NULL,
    faction         VARCHAR(64)     NOT NULL,      -- СЧЁС, МВД, Сталкер, ОПГ...
    rank            VARCHAR(64)     DEFAULT 'Гражданин',
    passport_id     VARCHAR(32)     UNIQUE,
    steam_id        BIGINT          UNIQUE,        -- связь с аккаунтом
    is_wanted       BOOLEAN         DEFAULT FALSE,
    wanted_level    SMALLINT        DEFAULT 0 CHECK (wanted_level BETWEEN 0 AND 5),
    is_monitored    BOOLEAN         DEFAULT FALSE,  -- флаг наблюдения СЧЁС
    created_at      TIMESTAMP       DEFAULT NOW(),
    last_seen       TIMESTAMP
);

-- === ЭКОНОМИКА ===

CREATE TABLE nbz_accounts (
    account_id      SERIAL          PRIMARY KEY,
    iin             CHAR(10)        UNIQUE REFERENCES nchg_citizen_registry(iin),
    balance_rub     BIGINT          DEFAULT 0 CHECK (balance_rub >= 0),
    frozen          BOOLEAN         DEFAULT FALSE,
    freeze_reason   TEXT,
    credit_limit    BIGINT          DEFAULT 0,
    credit_debt     BIGINT          DEFAULT 0,
    updated_at      TIMESTAMP       DEFAULT NOW()
);

CREATE TABLE nbz_transactions (
    trans_id        SERIAL          PRIMARY KEY,
    sender_iin      CHAR(10)        REFERENCES nchg_citizen_registry(iin),
    receiver_iin    CHAR(10)        REFERENCES nchg_citizen_registry(iin),
    amount_rub      BIGINT          NOT NULL,
    trans_type      VARCHAR(32)     NOT NULL,       -- 'transfer', 'sms_fee', 'call_fee', 'exploit_drain', 'laundering', 'deposit', 'credit_payment'
    is_shadow       BOOLEAN         DEFAULT FALSE,  -- теневая транзакция
    status          VARCHAR(16)     DEFAULT 'completed',  -- 'pending', 'completed', 'reversed'
    initiated_by    CHAR(10),                        -- IIN инициатора
    timestamp       TIMESTAMP       DEFAULT NOW()
);

CREATE TABLE shadow_accounts (
    iin             CHAR(10)        PRIMARY KEY REFERENCES nchg_citizen_registry(iin),
    balance_rub     BIGINT          DEFAULT 0,
    total_stolen    BIGINT          DEFAULT 0,
    laundering_pending BIGINT       DEFAULT 0        -- сумма в процессе отмывки
);

-- === КРЕДИТЫ ===

CREATE TABLE nbz_credits (
    credit_id       SERIAL          PRIMARY KEY,
    iin             CHAR(10)        REFERENCES nchg_citizen_registry(iin),
    credit_type     VARCHAR(32)     NOT NULL,        -- 'start', 'business', 'wheels', 'prestige', 'dark'
    amount_rub      BIGINT          NOT NULL,
    remaining_debt  BIGINT          NOT NULL,
    interest_rate   DECIMAL(8,4)    NOT NULL,        -- процент в час
    issued_at       TIMESTAMP       DEFAULT NOW(),
    due_by          TIMESTAMP       NOT NULL,
    status          VARCHAR(16)     DEFAULT 'active', -- 'active', 'overdue', 'closed'
    collateral      TEXT                             -- описание залога (для prestige)
);

-- === БЕЗОПАСНОСТЬ И СЧЁС ===

CREATE TABLE schs_security_log (
    event_id        SERIAL          PRIMARY KEY,
    attacker_iin    CHAR(10),                        -- может быть NULL если не определён
    target_iin      CHAR(10)        REFERENCES nchg_citizen_registry(iin),
    event_type      VARCHAR(32)     NOT NULL,        -- 'nmap_scan', 'exploit_attempt', 'exploit_success', 'shadow_transfer', 'spoof_detected'
    exploit_used    VARCHAR(32),
    detection_chance DECIMAL(5,4),                   -- 0.0000 - 1.0000
    was_detected    BOOLEAN         DEFAULT FALSE,
    payload_json    JSONB,
    timestamp       TIMESTAMP       DEFAULT NOW()
);

CREATE TABLE schs_monitoring_flags (
    flag_id         SERIAL          PRIMARY KEY,
    iin             CHAR(10)        REFERENCES nchg_citizen_registry(iin),
    reason          TEXT            NOT NULL,
    set_by          VARCHAR(128),
    is_active       BOOLEAN         DEFAULT TRUE,
    created_at      TIMESTAMP       DEFAULT NOW()
);

-- === КРИМИНАЛЬНАЯ ИСТОРИЯ ===

CREATE TABLE criminal_records (
    record_id       SERIAL          PRIMARY KEY,
    iin             CHAR(10)        REFERENCES nchg_citizen_registry(iin),
    article         VARCHAR(16)     NOT NULL,        -- 'УК.1.3', 'УК.7.1'...
    description     TEXT            NOT NULL,
    verdict         TEXT,
    status          VARCHAR(16)     DEFAULT 'active', -- 'active', 'expunged'
    date            DATE            DEFAULT CURRENT_DATE
);

-- Индексы
CREATE INDEX idx_transactions_sender ON nbz_transactions(sender_iin);
CREATE INDEX idx_transactions_receiver ON nbz_transactions(receiver_iin);
CREATE INDEX idx_transactions_timestamp ON nbz_transactions(timestamp DESC);
CREATE INDEX idx_security_log_target ON schs_security_log(target_iin);
CREATE INDEX idx_security_log_timestamp ON schs_security_log(timestamp DESC);
CREATE INDEX idx_citizen_faction ON nchg_citizen_registry(faction);