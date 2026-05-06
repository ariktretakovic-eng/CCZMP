-- ============================================================
-- pda_ui_admin.script
-- UI админ-панели
-- ============================================================

class "UIPdaAdmin" (CUIScriptWnd)

function UIPdaAdmin:__init()
    CUIScriptWnd.__init(self)
    self._mgr = nil
    self._active_tab = "main"
    self._cmd_history = {}
    self._history_pos = 0
end

function UIPdaAdmin:InitControls(xml_name)
    self:Init(xml_name, true)
    local xml = CScriptXmlInit()
    xml:ParseFile(xml_name)
    
    -- Заголовок
    self._btn_close = xml:InitButton("title_bar:btn_close", self)
    
    -- Вкладки
    self._tab_main     = xml:InitButton("tab_bar:tab_main", self)
    self._tab_items    = xml:InitButton("tab_bar:tab_items", self)
    self._tab_tp       = xml:InitButton("tab_bar:tab_tp", self)
    self._tab_players  = xml:InitButton("tab_bar:tab_players", self)
    self._tab_terminal = xml:InitButton("tab_bar:tab_terminal", self)
    
    -- Панели
    self._panel_main     = xml:InitWindow("panel_main", self)
    self._panel_items    = xml:InitWindow("panel_items", self)
    self._panel_tp       = xml:InitWindow("panel_tp", self)
    self._panel_players  = xml:InitWindow("panel_players", self)
    self._panel_terminal = xml:InitWindow("panel_terminal", self)
    
    -- Main
    self._lbl_status   = xml:InitStatic("panel_main:lbl_status", self)
    self._lbl_level    = xml:InitStatic("panel_main:lbl_level", self)
    self._btn_activate = xml:InitButton("panel_main:btn_activate", self)
    self._btn_deact    = xml:InitButton("panel_main:btn_deact", self)
    self._edit_code    = xml:InitEditBox("panel_main:edit_code", self)
    
    -- Items
    self._item_categories = xml:InitComboBox("panel_items:item_categories", self)
    self._item_list       = xml:InitListBox("panel_items:item_list", self)
    self._item_count      = xml:InitEditBox("panel_items:item_count", self)
    self._btn_spawn       = xml:InitButton("panel_items:btn_spawn", self)
    
    -- Teleport
    self._tp_list     = xml:InitListBox("panel_tp:tp_list", self)
    self._tp_x        = xml:InitEditBox("panel_tp:tp_x", self)
    self._tp_y        = xml:InitEditBox("panel_tp:tp_y", self)
    self._tp_z        = xml:InitEditBox("panel_tp:tp_z", self)
    self._btn_tp      = xml:InitButton("panel_tp:btn_tp", self)
    
    -- Terminal
    self._terminal_log  = xml:InitListBox("panel_terminal:terminal_log", self)
    self._cmd_input     = xml:InitEditBox("panel_terminal:cmd_input", self)
    
    -- Регистрация кнопок
    self:Register(self._btn_close, "btn_close")
    self:Register(self._tab_main, "tab_main")
    self:Register(self._tab_items, "tab_items")
    self:Register(self._tab_tp, "tab_tp")
    self:Register(self._tab_players, "tab_players")
    self:Register(self._tab_terminal, "tab_terminal")
    self:Register(self._btn_activate, "btn_activate")
    self:Register(self._btn_deact, "btn_deactivate")
    self:Register(self._btn_spawn, "btn_spawn")
    self:Register(self._btn_tp, "btn_tp")
    
    -- Начальное состояние
    self:_switch_tab("main")
    self:_populate_tp_list()
    self:_refresh_main_panel()
end

function UIPdaHacker:AttachModules(mgr)
    self._mgr = mgr
    self._admin_mod = mgr.modules["admin"]
    
    if self._admin_mod then
        self._admin_mod.set_on_state_change(function(state)
            self:_refresh_main_panel()
        end)
        self._admin_mod.set_on_log_update(function(msg_type, text)
            self:_add_terminal_line(msg_type, text)
        end)
    end
end

-- ============================================================
-- ОБРАБОТЧИК КНОПОК
-- ============================================================

function UIPdaAdmin:OnButton(btn_id)
    if btn_id == "btn_close" then
        self._mgr:close()
    elseif btn_id == "tab_main" then self:_switch_tab("main")
    elseif btn_id == "tab_items" then self:_switch_tab("items")
    elseif btn_id == "tab_tp" then self:_switch_tab("tp")
    elseif btn_id == "tab_players" then self:_switch_tab("players")
    elseif btn_id == "tab_terminal" then self:_switch_tab("terminal")
    elseif btn_id == "btn_activate" then
        self:_activate_admin()
    elseif btn_id == "btn_deactivate" then
        self:_deactivate_admin()
    elseif btn_id == "btn_spawn" then
        self:_spawn_item()
    elseif btn_id == "btn_tp" then
        self:_teleport()
    end
end

function UIPdaAdmin:OnKeyboard(key, key_action)
    if key_action ~= 1 then return CUIScriptWnd.OnKeyboard(self, key, key_action) end
    
    if key == DIK_keys.DIK_ESCAPE then
        self._mgr:close()
        return true
    end
    
    if self._active_tab ~= "terminal" then
        return CUIScriptWnd.OnKeyboard(self, key, key_action)
    end
    
    if key == DIK_keys.DIK_RETURN or key == DIK_keys.DIK_NUMPADENTER then
        local cmd = self._cmd_input:GetText()
        if cmd and #cmd > 0 then
            self:_execute_command(cmd)
            self._cmd_input:SetText("")
        end
        return true
    end
    
    return CUIScriptWnd.OnKeyboard(self, key, key_action)
end

-- ============================================================
-- ДЕЙСТВИЯ
-- ============================================================

function UIPdaAdmin:_activate_admin()
    local code = self._edit_code:GetText()
    if self._admin_mod then
        local ok, err = self._admin_mod.activate_admin(code)
        if ok then
            self:_add_terminal_line("success", "Админ-доступ активирован")
        else
            self:_add_terminal_line("info", err or "Ожидание ответа сервера...")
        end
    end
end

function UIPdaAdmin:_deactivate_admin()
    if self._admin_mod then
        self._admin_mod.deactivate_admin()
        self:_add_terminal_line("info", "Админ-доступ деактивирован")
    end
end

function UIPdaAdmin:_spawn_item()
    -- Получаем выбранный предмет и количество
    -- В реальной реализации: получение из UI элементов
    local item = "medkit" -- заглушка
    local count = 1
    if self._admin_mod then
        self._admin_mod.quick_spawn(item, count)
    end
end

function UIPdaAdmin:_teleport()
    -- Получаем координаты или выбранную локацию
    -- Заглушка
    if self._admin_mod then
        self._admin_mod.quick_tp("bar")
    end
end

function UIPdaAdmin:_execute_command(cmd)
    self:_add_terminal_line("input", "> " .. cmd)
    table.insert(self._cmd_history, cmd)
    self._history_pos = #self._cmd_history + 1
    
    if self._admin_mod then
        local ok, result = self._admin_mod.execute_command(cmd)
        if result then
            local msg_type = ok and "success" or "error"
            self:_add_terminal_line(msg_type, result)
        end
    end
end

-- ============================================================
-- УПРАВЛЕНИЕ ВКЛАДКАМИ
-- ============================================================

local PANELS = {"main", "items", "tp", "players", "terminal"}

function UIPdaAdmin:_switch_tab(tab_name)
    self._active_tab = tab_name
    for _, t in ipairs(PANELS) do
        local panel = self["_panel_" .. t]
        if panel then
            panel:Show(t == tab_name)
        end
    end
end

-- ============================================================
-- ОБНОВЛЕНИЕ UI
-- ============================================================

function UIPdaAdmin:_refresh_main_panel()
    if not self._admin_mod then return end
    local state = self._admin_mod.get_state()
    
    if self._lbl_status then
        self._lbl_status:SetText(state.is_admin and "АКТИВЕН" or "НЕ АКТИВЕН")
    end
    if self._lbl_level then
        self._lbl_level:SetText(state.admin_level_name or "Нет доступа")
    end
end

function UIPdaAdmin:_populate_tp_list()
    if not self._admin_mod then return end
    local locations = self._admin_mod.get_tp_locations()
    for _, loc in ipairs(locations) do
        local item = CUIListBoxItem(16)
        item:SetText(string.format("%s (%d, %d, %d)", loc.name, loc.x, loc.y, loc.z))
        item:SetData(loc.id)
        self._tp_list:AddExistingItem(item)
    end
end

function UIPdaAdmin:_add_terminal_line(msg_type, text)
    local prefix = {
        success = "[+] ",
        error   = "[-] ",
        info    = "[*] ",
        input   = "> ",
    }
    local formatted = (prefix[msg_type] or "") .. text
    local item = CUIListBoxItem(16)
    item:SetText(formatted)
    self._terminal_log:AddExistingItem(item)
    self._terminal_log:ScrollToEnd()
end

-- ============================================================
-- ФАБРИКА
-- ============================================================

function create_window(mgr, xml_name)
    local wnd = UIPdaAdmin()
    wnd:InitControls(xml_name)
    wnd:AttachModules(mgr)
    return wnd
end

return { create_window = create_window }