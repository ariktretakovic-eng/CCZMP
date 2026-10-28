"""Original item storage, PIN grants, save-state and timed intrusion regressions."""
import unittest
import test_items as T
from test_continuation import COOLER_PRE
PRE=COOLER_PRE.replace('local cooler=actor_item("cczmp_cooler")','local cooler=actor_item("cczmp_code_case")').replace('s.container={','s.vault={revision=0,attempts=0,container={').replace('contents={}}\nfunction transfer','contents={}}}\nfunction transfer')+r'''
IsHeadgear=function(x)return x and x.helmet end
system_ini=function()return {line_exist=function()return false end,section_exist=function()return true end,r_string=function(self,s,k)return s end}end
function vector()return {set=function(self,p)self.x=p.x or 0;self.y=p.y or 0;self.z=p.z or 0;return self end}end
function cargo(mass)
 local o=actor_item("cczmp_components");function o:weight()return mass or .5 end
 return o
end
local pick=actor_item("cczmp_code_pick")
function setup_pin()
 assert(cczmp_locks.configure(cooler:id(),"0012"));assert(not cczmp_locks.access(cooler:id()))
end
'''
CASES={
'PIN_validation_initial_close_and_leading_zero':PRE+r'''
assert(cczmp_locks.access(cooler:id()));for _,pin in ipairs({"123","123456789","12 34","abcd"})do assert(not cczmp_locks.configure(cooler:id(),pin))end
setup_pin();assert(not cczmp_locks.unlock(cooler:id(),"12"));assert(cczmp_locks.unlock(cooler:id(),"0012"));assert(cczmp_locks.access(cooler:id()))
assert(cczmp_locks.close(cooler:id()));assert(not cczmp_locks.access(cooler:id()))
''',
'PIN_three_errors_persistent_cooldown':PRE+r'''
setup_pin();for i=1,3 do assert(not cczmp_locks.unlock(cooler:id(),"0000"))end
assert(not cczmp_locks.unlock(cooler:id(),"0012"));assert(cczmp_locks.info(cooler:id()).cooldown==300)
cczmp_locks.on_game_start();callbacks.on_game_load();clock=clock+299;assert(not cczmp_locks.unlock(cooler:id(),"0012"))
clock=clock+1;assert(cczmp_locks.unlock(cooler:id(),"0012"));assert(cczmp_locks.info(cooler:id()).attempts==0)
''',
'PIN_grant_expiry_and_cold_load':PRE+r'''
setup_pin();assert(cczmp_locks.unlock(cooler:id(),"0012"));clock=clock+119;assert(cczmp_locks.access(cooler:id()))
clock=clock+1;assert(not cczmp_locks.access(cooler:id()));assert(cczmp_locks.unlock(cooler:id(),"0012"))
cczmp_locks.on_game_start();callbacks.on_game_load();assert(not cczmp_locks.access(cooler:id()));assert(cczmp_locks.unlock(cooler:id(),"0012"))
''',
'original_cargo_condition_storage_and_single_take':PRE+r'''
local a=cargo();a.cond=.73;assert(cczmp_locks.store(cooler:id(),a:id()));assert(cooler.mass==1.7)
setup_pin();assert(not cczmp_locks.take(cooler:id(),a:id()));assert(#cczmp_locks.contents(cooler:id())==0)
assert(cczmp_locks.unlock(cooler:id(),"0012"));assert(cczmp_locks.take(cooler:id(),a:id()))
assert(db.actor:object_id(a:id())==a and a.cond==.73 and cooler.mass==1.2);assert(not cczmp_locks.take(cooler:id(),a:id()))
''',
'capacity_12_and_max_mass':PRE+r'''
for i=1,12 do assert(cczmp_locks.store(cooler:id(),cargo():id()))end
local o=cargo();assert(not cczmp_locks.store(cooler:id(),o:id()));assert(cczmp_items.owned(o:id()));assert(#cczmp_locks.contents(cooler:id())==12)
''',
'max_mass_rejects_before_transfer':PRE+r'''
local a=cargo(10);assert(cczmp_locks.store(cooler:id(),a:id()));local b=cargo(.01)
assert(not cczmp_locks.store(cooler:id(),b:id()));assert(cczmp_items.owned(b:id()));assert(cooler.mass==11.2)
''',
'no_nested_containers_quest_or_equipment':PRE+r'''
local art=artifact();assert(not cczmp_locks.store(cooler:id(),art:id()));assert(not cczmp_locks.store(cooler:id(),cooler:id()))
local nested=actor_item("cczmp_cooler");assert(not cczmp_locks.store(cooler:id(),nested:id()))
local gun=cargo();gun.weapon=true;assert(not cczmp_locks.store(cooler:id(),gun:id()))
local q=cargo();system_ini=function()return {line_exist=function()return true end,r_bool=function()return true end}end
assert(not cczmp_locks.store(cooler:id(),q:id()));assert(#cczmp_locks.contents(cooler:id())==0)
''',
'box_identity_and_no_failed_creation_consumption':PRE+r'''
local o=cargo();local s=cczmp_items.item_state(cooler);s.vault.container=nil;spawn_fault=true
assert(not cczmp_locks.store(cooler:id(),o:id()));assert(cczmp_items.owned(o:id()));assert(not s.vault.container)
s.vault.container={id=5000,name=box:name(),level="test_level",contents={}};spawn_fault=false
assert(cczmp_locks.store(cooler:id(),o:id()));box.nname="replacement";assert(not cczmp_locks.take(cooler:id(),o:id()))
''',
'failed_transfer_does_not_record_or_duplicate':PRE+r'''
local o=cargo();db.actor.transfer_item=function()end;assert(cczmp_locks.store(cooler:id(),o:id()))
assert(#cczmp_locks.contents(cooler:id())==0 and cczmp_items.owned(o:id()));clock=clock+30;assert(#cczmp_locks.contents(cooler:id())==0);assert(not cczmp_items.item_state(cooler).vault.container.pending)
''',
'code_pick_timed_success_energy_and_skill':PRE+r'''
setup_pin();world.cczmp_items.skills.technology.level=0;assert(not cczmp_hacking.start("code_pick",pick:id(),cooler:id()))
world.cczmp_items.skills.technology.level=1;assert(cczmp_hacking.start("code_pick",pick:id(),cooler:id()))
assert(not cczmp_hacking.finish_job());assert(not cczmp_locks.access(cooler:id()));assert(complete(true))
assert(cczmp_locks.access(cooler:id()));assert(cczmp_items.item_state(pick).charge==85)
assert(world.cczmp_items.skills.technology.xp==2)
''',
'code_pick_failure_cooldown_no_generic_day_lock':PRE+r'''
setup_pin();assert(cczmp_hacking.start("code_pick",pick:id(),cooler:id()));assert(not complete(false))
assert(not cczmp_locks.access(cooler:id()));assert(cczmp_items.item_state(pick).charge==85 and not cczmp_items.item_state(pick).lock)
assert(not cczmp_hacking.start("code_pick",pick:id(),cooler:id()));clock=clock+30
assert(cczmp_hacking.start("code_pick",pick:id(),cooler:id()));assert(complete(true))
''',
'code_pick_lost_or_reused_target_no_cost':PRE+r'''
setup_pin();assert(cczmp_hacking.start("code_pick",pick:id(),cooler:id()));cooler.nname="new_instance"
assert(not complete(true));assert(cczmp_items.item_state(pick).charge==100)
''',
'code_pick_PIN_revision_and_cancel_no_cost':PRE+r'''
setup_pin();assert(cczmp_hacking.start("code_pick",pick:id(),cooler:id()));assert(cczmp_locks.unlock(cooler:id(),"0012"));assert(cczmp_locks.configure(cooler:id(),"9999"))
assert(not complete(true));assert(cczmp_items.item_state(pick).charge==100)
assert(cczmp_hacking.start("code_pick",pick:id(),cooler:id()));assert(cczmp_hacking.cancel());assert(cczmp_items.item_state(pick).charge==100)
''',
'code_pick_missing_tool_power_and_unarmed':PRE+r'''
assert(not cczmp_hacking.start("code_pick",pick:id(),cooler:id()));setup_pin();assert(not cczmp_hacking.start("code_pick",cooler:id(),cooler:id()))
cczmp_items.item_state(pick).charge=14;assert(not cczmp_hacking.start("code_pick",pick:id(),cooler:id()));assert(not cczmp_items.world().job)
''',
'code_pick_save_job_and_recharge':PRE+r'''
setup_pin();assert(cczmp_hacking.start("code_pick",pick:id(),cooler:id()));cczmp_locks.on_game_start();callbacks.on_game_load()
assert(complete(true));cczmp_items.item_state(pick).charge=0;actor_item("cczmp_battery_device");assert(cczmp_items.recharge(pick:id()))
assert(cczmp_items.item_state(pick).charge==100)
''',
'case_UI_prompt_back_and_reused_identity':PRE+r'''
local c=cczmp_ui.get_ctrl();c.items_selected=cooler:id();c.page="items_case";c:refresh();c:handle_action("items_pin:configure");c:refresh()
assert(c.page=="items_pin_prompt"and cczmp_items_ui.is_prompt(c.page));c.input="0012";assert(c:handle_action("items_pin_confirm")=="cczmp_locks_configured");assert(c.page=="items_case")
c:handle_action("items_pin:unlock");c.input="0012";c:back();assert(c.page=="items_case"and c.input=="")
c:handle_action("items_pin:unlock");c.input="0012";cooler.nname="replacement";assert(c:handle_action("items_pin_confirm")=="cczmp_locks_changed")
''',
'case_purchase_stock_cash_spawn_failure_and_debug':PRE+r'''
local n={name=function()return "trader1"end,character_name=function()return "Trader"end};cczmp_items.nearest_trader=function()return n end;db.actor.cash=100000
assert(cczmp_gear.buy("cczmp_code_case"));assert(db.actor.cash==88000)
assert(cczmp_gear.buy("cczmp_code_case"));assert(db.actor.cash==76000);assert(not cczmp_gear.buy("cczmp_code_case"));assert(db.actor.cash==76000)
spawn_fault=true;assert(not cczmp_gear.buy("cczmp_code_pick"));assert(db.actor.cash==76000)
DEV_DEBUG=false;assert(not cczmp_items.spawn("cczmp_code_pick",true))
''',
}
CASES['native_headgear_helper_in_case_and_workshop']=PRE+r'''
IsHelmet=nil;local h=actor_item("cczmp_helmet_tactical");h.helmet=true
assert(not cczmp_locks.storable(h));local c=cczmp_ui.get_ctrl();c.page="items_workshop";c:refresh()
local found=false;for _,r in ipairs(c.lines)do if r.act=="items_workshop_repair:"..h:id()then found=true end end;assert(found)
assert(not cczmp_engineering.workshop(h:id()))
'''
CASES['deferred_transfer_once_and_original_identity']=PRE+r'''
local o=cargo();local queued=0;db.actor.transfer_item=function(self,item,to)queued=queued+1;deferred=function()transfer(self,item,to)end end
assert(cczmp_locks.store(cooler:id(),o:id()));assert(not cczmp_locks.store(cooler:id(),o:id()));assert(queued==1 and #cczmp_locks.contents(cooler:id())==0)
deferred();assert(#cczmp_locks.contents(cooler:id())==1 and cooler.mass==1.7)
box.transfer_item=function(self,item,to)queued=queued+1;deferred=function()transfer(self,item,to)end end
assert(cczmp_locks.take(cooler:id(),o:id()));assert(not cczmp_locks.take(cooler:id(),o:id()));assert(queued==2)
deferred();assert(#cczmp_locks.contents(cooler:id())==0 and db.actor:object_id(o:id())==o and cooler.mass==1.2)
'''
CASES['pending_transfer_saved_and_locked_on_load']=PRE+r'''
local o=cargo();db.actor.transfer_item=function(self,item,to)deferred=function()transfer(self,item,to)end end
assert(cczmp_locks.store(cooler:id(),o:id()));setup_pin();cczmp_locks.on_game_start();callbacks.on_game_load();deferred()
frame=4000;callbacks.actor_on_update();assert(not cczmp_locks.access(cooler:id()));assert(not cczmp_items.item_state(cooler).vault.container.pending)
assert(cczmp_locks.unlock(cooler:id(),"0012"));assert(#cczmp_locks.contents(cooler:id())==1)
'''
CASES['native_attachment_condition_reset_restored_on_original']=PRE+r'''
local o=cargo();o.cond=.73;assert(cczmp_locks.store(cooler:id(),o:id()));setup_pin()
o.cond=1;cczmp_locks.on_game_start();callbacks.on_game_load();frame=4000;callbacks.actor_on_update()
assert(o.cond==.73);assert(cczmp_locks.unlock(cooler:id(),"0012"));assert(cczmp_locks.take(cooler:id(),o:id()))
assert(db.actor:object_id(o:id())==o and o.cond==.73)
'''
class Locks(T.Items):pass
for name in dir(T.Items):
 if name.startswith('test_'):setattr(Locks,name,None)
for name,script in CASES.items():setattr(Locks,'test_'+name,lambda self,s=script:self.run_case(s))
if __name__=='__main__':unittest.main(verbosity=2)
