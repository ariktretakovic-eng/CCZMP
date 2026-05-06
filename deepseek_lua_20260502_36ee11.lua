-- ============================================================
-- bind_stalker.script
-- Главный файл инициализации CCZMP
-- Подключает все модули и регистрирует коллбэки
-- ============================================================

-- Флаг инициализации
local cczmp_initialized = false

-- ============================================================
-- ФУНКЦИЯ ИНИЦИАЛИЗАЦИИ CCZMP
-- ============================================================

function initialize_cczmp()
    if cczmp_initialized then
        printf("[CCZMP] Уже инициализировано, пропускаем")
        return
    end
    
    printf("============================================")
    printf("[CCZMP] Инициализация Chernobyl Criminal Zone")
    printf("============================================")
    
    -- 1. Инициализация шины событий
    local ok, cczmp_events = pcall(require, "cczmp.cczmp_events")
    if not ok then
        printf("[CCZMP] ERROR: не удалось загрузить cczmp_events: " .. tostring(cczmp_events))
        return
    end
    _G.cczmp_events = cczmp_events
    printf("[CCZMP] Шина событий загружена")
    
    -- 2. Инициализация PDA Manager
    local ok, pda_manager = pcall(require, "cczmp.pda_manager")
    if ok and pda_manager then
        _G.pda_manager = pda_manager
        printf("[CCZMP] PDA Manager загружен")
        
        -- Регистрируем коллбэк использования предмета КПК
        RegisterScriptCallback("actor_item_use", function(item)
            local section = item:section()
            local mgr = pda_manager.get()
            if mgr and pda_manager.get_device_config(section) then
                local actor = db.actor
                if actor then
                    mgr:set_active_device(section, actor:id())
                    mgr:open()
                end
            end
        end)
        printf("[CCZMP] Callback actor_item_use зарегистрирован")
    else
        printf("[CCZMP] WARN: pda_manager не загружен")
    end
    
    -- 3. Активация оффлайн-админа (временно, удалить перед релизом)
    if not is_multiplayer() then
        printf("[CCZMP] Обнаружен оффлайн-режим, активирую админ-доступ")
        local ok, admin_mod = pcall(require, "cczmp.pda_module_admin")
        if ok and admin_mod then
            admin_mod.activate_admin()
        end
    end
    
    -- 4. Регистрация коллбэка на смерть (закрыть КПК)
    RegisterScriptCallback("actor_on_before_death", function()
        local mgr = _G.pda_manager and _G.pda_manager.get()
        if mgr and mgr.is_open then
            mgr:close()
        end
    end)
    
    cczmp_initialized = true
    printf("[CCZMP] Инициализация завершена")
end

-- ============================================================
-- ТОЧКИ ВХОДА (X-Ray Callbacks)
-- ============================================================

-- Вызывается при старте новой игры
function on_game_start()
    printf("[CCZMP] on_game_start triggered")
    initialize_cczmp()
end

-- Вызывается при загрузке сохранения
function on_game_load()
    printf("[CCZMP] on_game_load triggered")
    -- Небольшая задержка, чтобы движок загрузил все объекты
    CreateTimeEvent("cczmp_init_delay", "delayed_init", 1.0)
end

function delayed_init()
    initialize_cczmp()
    return true  -- true = удалить таймер после выполнения
end

-- Очистка при выходе
function on_game_exit()
    local mgr = _G.pda_manager and _G.pda_manager.get()
    if mgr then
        mgr:_unload_modules()
    end
    printf("[CCZMP] Модули выгружены")
end

-- ============================================================
-- ПРОВЕРКА РЕЖИМА
-- ============================================================

function is_multiplayer()
    -- В Anomaly 1.5.3 проверяем через level
    local ok, result = pcall(function()
        return level.is_server()
    end)
    return ok and result
end

-- ============================================================
-- УТИЛИТЫ
-- ============================================================

function printf(msg)
    -- Вывод в консоль и лог X-Ray
    print(msg)
end