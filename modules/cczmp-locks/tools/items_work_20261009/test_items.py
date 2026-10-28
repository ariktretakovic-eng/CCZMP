from pathlib import Path
import configparser,json,unittest,sys
from lupa.luajit21 import LuaRuntime
WORK=Path(__file__).resolve().parent;ROOT=WORK.parents[1];STAGE=ROOT
sys.path.insert(0,str(ROOT/'tools/tests'))
from test_cczmp_operations import SETUP as BASE
SETUP=BASE+r'''
next_item=1000; DEV_DEBUG=true; frame=0
function time_global() return frame end
function IsOutfit(o)return o and o.outfit end
function IsWeapon(o)return o and o.weapon end
function actor_item(s,owner)
 local o=owner or db.actor;next_item=next_item+1;local id=next_item
 local t={nid=id,nname=s.."_"..id,sec=s,owner=o,cond=.5}
 function t:id()return self.nid end
 function t:name()return self.nname end
 function t:section()return self.sec end
 function t:parent()return self.owner end
 function t:condition()return self.cond end
 function t:set_condition(c)self.cond=c end
 o.items[#o.items+1]=t;objects[id]=t;server[id]={}
 return t
end
function bind_inventory(o)
 function o:object(key)
  if type(key)=="number"then return self.items[key+1] end
  for _,t in ipairs(self.items)do if t:section()==key then return t end end
 end
 function o:object_id(key)
  for _,t in ipairs(self.items)do if t:id()==key then return t end end
 end
 function o:level_vertex_id()return 1 end
 function o:game_vertex_id()return 1 end
end
bind_inventory(db.actor);bind_inventory(npc)
function alife_release(item)
 assert(item and objects[item:id()])
 local o=item:parent();for i,t in ipairs(o.items)do if t:id()==item:id()then table.remove(o.items,i);break end end
 objects[item:id()]=nil;server[item:id()]=nil
end
function alife_create(s,p,l,g,parent)
 if spawn_fault then return nil end
 local item=actor_item(s)
 return {id=item:id(),name=function()return item:name()end}
end
function system_ini()return {section_exist=function(self,s)return true end}end
function hide_hud_inventory()end
game.translate_string=function(s)return s end
level.name=function()return "test_level" end
game_object={enemy=1}
trade_manager={get_trade_profile=function()return nil end}
cczmp_factions.all=function()return {"mvd","cobra"}end
cczmp_factions.get_name=function(s)return s end
cczmp_factions.get_location=function(s)return "base" end
function skills(eng,tech,radio)
 world.cczmp_items=nil;local w=cczmp_items.world()
 w.skills={engineer={level=eng or 3,xp=0},technology={level=tech or 3,xp=0},radio={level=radio or 3,xp=0}}
end
function complete(success,detected)
 local j=cczmp_items.world().job;assert(j)
 j.fail_roll=success and 10000 or 1;j.detect_roll=detected and 1 or 10000
 clock=clock+j.seconds
 return cczmp_hacking.finish_job()
end
function supply_recipe(id)
 local cfg=configs["cczmp/items.ltx"]["recipe_"..id]
 for s,n in cfg.materials:gmatch("([%w_]+):(%d+)")do for i=1,tonumber(n)do actor_item(s)end end
 for s in cfg.tools:gmatch("[^,%s]+")do actor_item(s)end
end
'''
CASES={
 'PDA_timed_capture':r'''skills();setup_target();actor_item("device_pda_1",npc);local p=actor_item("device_pda_2");actor_item("cczmp_programmer")
 assert(cczmp_hacking.start("pda_1",p:id(),key));assert(not cczmp_hacking.finish_job());assert(not world.cczmp_operations.services["hacked_"..key])
 assert(complete(true));local r=world.cczmp_operations.services["hacked_"..key];assert(r.money==500 and r.name=="Citizen")
 assert(cczmp_items.item_state(p).charge==90)''',
 'missing_programmer_no_state_change':r'''skills();setup_target();actor_item("device_pda_1",npc);actor_item("device_pda_2")
 assert(not cczmp_hacking.start("pda_1",nil,key));assert(not cczmp_items.world().job)''',
 'skills_and_target_level':r'''skills(3,1);setup_target();actor_item("device_pda_2",npc);actor_item("device_pda_3");actor_item("cczmp_programmer")
 assert(not cczmp_hacking.start("pda_1",nil,key));world.cczmp_items.skills.technology.level=3
 assert(not cczmp_hacking.start("pda_1",nil,key));actor_item("cczmp_jtag");assert(cczmp_hacking.start("pda_2",nil,key))''',
 'blocked_24_hours_and_downgrade':r'''skills();setup_target();actor_item("device_pda_1",npc);local p=actor_item("device_pda_3");actor_item("cczmp_jtag")
 assert(cczmp_hacking.start("pda_2",nil,key));assert(not complete(false));local s=cczmp_items.item_state(p);assert(s.lock and s.grade==2)
 assert(not cczmp_items.usable(p,0));clock=clock+86401;assert(cczmp_items.usable(p,0));assert(not s.lock)''',
 'reused_item_id_aborts':r'''skills();setup_target();actor_item("device_pda_1",npc);local p=actor_item("device_pda_2");actor_item("cczmp_programmer")
 assert(cczmp_hacking.start("pda_1",nil,key));p.nname="replacement";assert(not complete(true));assert(not world.cczmp_operations.services["hacked_"..key])''',
 'target_gone_aborts':r'''skills();setup_target();actor_item("device_pda_1",npc);actor_item("device_pda_2");actor_item("cczmp_programmer")
 assert(cczmp_hacking.start("pda_1",nil,key));npc.dead=true;assert(not complete(true));assert(not world.cczmp_operations.services["hacked_"..key])''',
 'materials_lost_during_job':r'''skills();local p=actor_item("cczmp_laptop_multi");actor_item("cczmp_usb_os");local os=actor_item("cczmp_os_linux")
 assert(cczmp_hacking.start("os_laptop",p:id()));alife_release(os);assert(not complete(true));assert(cczmp_items.item_state(p).os=="civil")''',
 'OS_change_consumes_only_license':r'''skills();local p=actor_item("cczmp_laptop_multi");local usb=actor_item("cczmp_usb_os");actor_item("cczmp_os_linux")
 assert(cczmp_hacking.start("os_laptop",p:id()));assert(complete(true));assert(cczmp_items.item_state(p).os=="linux");assert(db.actor:object_id(usb:id()));assert(not db.actor:object("cczmp_os_linux"))''',
 'fixed_laptop_all_OS_blocked':r'''skills();role("mvd",24);local p=actor_item("cczmp_laptop_basic");actor_item("cczmp_usb_os");actor_item("cczmp_os_linux")
 assert(not cczmp_hacking.start("os_laptop",p:id()));assert(not cczmp_hacking.start("gov_os",p:id()))''',
 'ghost_only_secure':r'''skills();local p=actor_item("cczmp_phone_basic");actor_item("cczmp_usb_os");actor_item("cczmp_os_ghost")
 assert(not cczmp_hacking.start("ghost",p:id()));local q=actor_item("cczmp_phone_secure");assert(cczmp_hacking.start("ghost",q:id()));assert(complete(true));assert(cczmp_items.item_state(q).os=="ghost")''',
 'role_change_gov_job':r'''skills();role("mvd",24);local p=actor_item("cczmp_laptop_multi");actor_item("cczmp_usb_os")
 assert(cczmp_hacking.start("gov_os",p:id()));role("cobra");assert(not complete(true));assert(cczmp_items.item_state(p).os=="civil")''',
 'two_jobs_and_cancel':r'''skills();supply_recipe("battery");assert(cczmp_engineering.start("battery"));assert(not cczmp_engineering.start("battery"));assert(cczmp_hacking.cancel());assert(db.actor:object("cczmp_cell"))''',
 'craft_quantities_and_tools_kept':r'''skills();supply_recipe("battery");assert(cczmp_engineering.start("battery"));clock=clock+1800;assert(cczmp_engineering.finish_job())
 assert(db.actor:object("cczmp_battery_device"));assert(not db.actor:object("cczmp_cell"));assert(not db.actor:object("cczmp_copper_wire"));assert(db.actor:object("cczmp_toolset"))''',
 'failed_spawn_preserves_materials':r'''skills();supply_recipe("battery");assert(cczmp_engineering.start("battery"));spawn_fault=true;clock=clock+1800;assert(not cczmp_engineering.finish_job())
 assert(db.actor:object("cczmp_cell") and db.actor:object("cczmp_copper_wire"));assert(not db.actor:object("cczmp_battery_device"))''',
 'recharge_consumes_exactly_one':r'''skills();local p=actor_item("cczmp_phone_basic");cczmp_items.item_state(p).charge=20;local b1=actor_item("cczmp_battery_device");local b2=actor_item("cczmp_battery_device")
 assert(cczmp_items.recharge(p:id()));assert(cczmp_items.item_state(p).charge==100);assert(not db.actor:object_id(b1:id()));assert(db.actor:object_id(b2:id()))''',
 'repair_no_duplicate_and_clamp':r'''skills();local p=actor_item("armor");p.outfit=true;p.cond=.9;local k=actor_item("cczmp_repair_armor")
 assert(cczmp_engineering.repair(p:id(),k:id()));assert(p.cond==1);assert(not db.actor:object_id(k:id()));assert(not cczmp_engineering.repair(p:id(),k:id()))''',
 'clone_criminal_alternative':r'''skills(0,0);role("cobra");local p=actor_item("cczmp_bank_card");actor_item("cczmp_blank_card");actor_item("cczmp_card_reader")
 assert(cczmp_hacking.start("clone_card",p:id()));assert(complete(true));assert(db.actor:object("cczmp_cloned_card"));assert(not db.actor:object("cczmp_blank_card"))''',
 'detected_incident':r'''skills();setup_target();actor_item("device_pda_1",npc);actor_item("device_pda_2");actor_item("cczmp_programmer")
 assert(cczmp_hacking.start("pda_1",nil,key));assert(complete(true,true));local found=false;for _,r in pairs(world.cczmp_operations.incidents)do if r.kind=="device_intrusion_detected"then found=true end end;assert(found)''',
 'job_reload_same_state':r'''skills();local p=actor_item("cczmp_laptop_multi");actor_item("cczmp_usb_os");actor_item("cczmp_os_linux");assert(cczmp_hacking.start("os_laptop",p:id()))
 local w=world;cczmp_hacking.on_game_start();callbacks.on_game_load();clock=clock+1800;assert(cczmp_hacking.finish_job());assert(world==w and cczmp_items.item_state(p).os=="linux")''',
 'all_recipes_start_and_finish':r'''for _,r in ipairs(cczmp_engineering.recipes())do db.actor.items={};skills();supply_recipe(r);assert(cczmp_engineering.start(r));assert(not cczmp_engineering.finish_job());clock=clock+cczmp_items.number("recipe_"..r,"seconds",1800)+1;assert(cczmp_engineering.finish_job(),r)end''',
 'UI_round_trip_and_debug_guard':r'''skills();local c=cczmp_ui.get_ctrl();c.page="items_home";c:refresh();assert(#c.lines>4);c:handle_action("goto:items_recipes");assert(c.page=="items_recipes");c:back();assert(c.page=="items_home")
 c.page="items_debug";c.debug_mode=false;assert(c:handle_action("items_spawn:cczmp_phone_basic")=="cczmp_items_no_permission");c.debug_mode=true;assert(c:handle_action("items_spawn:cczmp_phone_basic")=="cczmp_items_spawned");assert(db.actor:object("cczmp_phone_basic"))''',
 'journal_bounded_and_primitives':r'''skills();for i=1,105 do cczmp_items.record("test","t",{v=i})end;assert(#cczmp_items.world().journal==100)
 local function scan(t)for k,v in pairs(t)do assert(type(v)~="userdata" and type(v)~="function");if type(v)=="table"then scan(v)end end end;scan(cczmp_items.world())''',
}

EXTRA=r"""
function IsMonster(n)return false end
function IsStalker(n)return n and n.human end
function setup_actor_fields(n)
 n.health=.5;n.power=.5;n.radiation=.4;n.bleeding=.1
 function n:set_health_ex(v)self.health=v end
 function n:relation()return 0 end
end
setup_actor_fields(db.actor);setup_actor_fields(npc)
hit={radiation=3,telepatic=4,chemical_burn=2,wound=6,fire_wound=8}
actor_menu={set_msg=function(...)end}
CInventory__eat=function(item)return true end
function db.actor:eat(item)
 callbacks.actor_on_item_use(item)
 item.uses=(item.uses or cczmp_items.number("item_"..item:section(),"doses",1))-1
 if item.uses<=0 then alife_release(item)end
end
function service(id,faction,rank)
 local n=make_npc(id,faction.."_"..id,0);bind_inventory(n);setup_actor_fields(n)
 n.community=faction;n.org_rank=rank or 2;n.role_name=nil
 return n
end
function clinic(role,id)
 local n=service(id or 3,"minzdrav",role=="radiologist" and 3 or 2);n.role_name=role
 return n
end
cczmp_professions.nearest=function(role)
 for _,e in pairs(db.storage)do if e.object.role_name==role and e.object.x<=4 and e.object:alive()then return e.object end end
end
cczmp_medicine.on_game_start()
"""
CASES.update({
 'deferred_release_cannot_double_spend':r'''skills();local p=actor_item("cczmp_cell");alife_release=function(item)end
 assert(cczmp_items.consume({cczmp_items.token(p)}));assert(not cczmp_items.owned(p:id()));assert(not cczmp_items.consume({cczmp_items.token(p)}));assert(not cczmp_items.select_materials("cczmp_cell:1"))''',
 'license_issuer_cash_and_physical_identity':r'''skills();db.actor.cash=20000;local n=service(3,"mvd",1)
 assert(cczmp_licenses.buy("D"));assert(db.actor.cash==15000);assert(cczmp_licenses.has("D"));assert(not cczmp_licenses.buy("D"))
 local l=db.actor:object("cczmp_license_d");l.nname="forgery";assert(not cczmp_licenses.has("D"))''',
 'license_requires_category_A_certificate':r'''skills();db.actor.cash=200000;service(3,"mo",2)
 assert(not cczmp_licenses.buy("A"));assert(db.actor.cash==200000);assert(cczmp_licenses.debug_issue("certificate"));assert(cczmp_licenses.buy("A"));assert(db.actor.cash==50000);assert(cczmp_licenses.has("A"))''',
 'empty_permit_and_debug_guard':r'''skills();actor_item("cczmp_license_a");assert(not cczmp_licenses.has("A"));DEV_DEBUG=false;assert(not cczmp_licenses.debug_issue("A"))''',
 'prescription_owner_expiry_and_pharmacy_stock':r'''skills();db.actor.cash=10000;clinic("doctor",3);clinic("pharmacist",4)
 assert(not cczmp_medicine.buy("cczmp_med_antibiotic"));assert(cczmp_medicine.request_prescription("cczmp_med_antibiotic"));assert(cczmp_medicine.buy("cczmp_med_antibiotic"));assert(db.actor.cash==6000);assert(not cczmp_medicine.buy("cczmp_med_antibiotic"))
 clock=clock+7*86400;assert(not cczmp_medicine.find_prescription("cczmp_med_antibiotic",true));assert(not cczmp_medicine.allowed(db.actor:object("cczmp_med_antibiotic")))''',
 'five_day_course_and_dose_interval':r'''skills();clinic("doctor",3);assert(cczmp_medicine.request_prescription("cczmp_med_antibiotic"));cczmp_medicine.infect("pneumonia")
 local med=actor_item("cczmp_med_antibiotic");assert(cczmp_medicine.use(med:id()));assert(not cczmp_medicine.allowed(med));assert(#cczmp_medicine.health_info().diseases==1)
 for i=2,5 do clock=clock+86400;assert(cczmp_medicine.use(med:id()))end
 assert(#cczmp_medicine.health_info().diseases==0);assert(not db.actor:object("cczmp_med_antibiotic"))''',
 'rx_native_eat_gate_and_patient_forgery':r'''skills();local med=actor_item("cczmp_med_serum");assert(CInventory__eat(med)==false,"missing RX accepted");assert(db.actor:object_id(med:id()),"medicine consumed");clinic("infectologist",3);assert(cczmp_medicine.request_prescription(med:section()),"RX denied");assert(CInventory__eat(med)~=false,"valid RX denied")
 local paper=db.actor:object("cczmp_prescription");local proof=alife_storage_manager.get_se_obj_state(alife():object(paper:id()),false).cczmp_prescription;proof.owner="another_patient";assert(CInventory__eat(med)==false,"foreign owner accepted")''',
 'specialist_hospital_and_invalid_patient':r'''skills();clinic("doctor",3);cczmp_medicine.infect("rad3");assert(not cczmp_medicine.hospital());clinic("radiologist",4);assert(not cczmp_medicine.hospital("missing"));assert(cczmp_medicine.hospital());assert(db.actor.health==1 and db.actor.radiation==0);assert(#cczmp_medicine.health_info().diseases==0)''',
 'native_medicine_health_and_protection':r'''skills();local med=actor_item("cczmp_med_medkit_small");assert(cczmp_medicine.use(med:id()));assert(db.actor.health==.7)
 local iodine=actor_item("cczmp_med_iodine");assert(cczmp_medicine.use(iodine:id()));local h={type=hit.radiation,power=.2};callbacks.actor_on_before_hit(h);assert(h.power==.1)''',
 'course_charges_effective_organization_rank':r'''skills(0,0,0);role("comnet",1);db.actor.cash=100000;local n=service(3,"scientists",2)
 trade_manager.get_trade_profile=function(id,k)return id==n:id() and "trade_stalker_owl.ltx" or nil end
 assert(cczmp_items.skill("radio")==2);assert(cczmp_items.train("radio"));assert(db.actor.cash==60000);assert(cczmp_items.skill("radio")==3)''',
 'vehicle_repair_health_and_destroyed_gate':r'''skills();local car={health=.5};function car:GetfHealth()return self.health end;function car:SetfHealth(v)self.health=v end
 local v=actor_item("vehicle");function v:get_car()return car end
 cczmp_vehicles={nearby=function()return {{id=v:id(),name=v:name()}}end}
 local kit=actor_item("cczmp_repair_mechanical");assert(cczmp_engineering.repair_vehicle(v:id(),kit:id()));assert(car.health==.75);assert(not cczmp_engineering.repair_vehicle(v:id(),kit:id()))
 car.health=0;kit=actor_item("cczmp_repair_mechanical");assert(not cczmp_engineering.repair_vehicle(v:id(),kit:id()));assert(db.actor:object_id(kit:id()))'''
})

GEAR_EXTRA=r"""
cczmp_factions.get_type=function(f)return (f=="cobra" and "criminal")or(f=="mvd" and "state")or"neutral"end
function db.actor:item_in_slot(id)return (self.slots or {})[id]end
function db.actor:get_bone_id(name)return name=="bip01_head" and 1 or name=="bip01_spine" and 2 or -1 end
function npc:active_item()return self.active_weapon end
function npc:direction()return {x=0,z=1}end
function db.actor:direction()return {x=0,z=1}end
IsArtefact=function(x)return x and x.artifact end
function friendly_trader()
 local n=service(3,"civilians",0)
 cczmp_items.nearest_trader=function()return n end
 return n
end
cczmp_gear.on_game_start()
"""
CASES.update({
 'catalog_purchase_license_and_stock':r"""skills();friendly_trader();db.actor.cash=500000
 assert(not cczmp_gear.buy("wpn_cczmp_pm"));assert(db.actor.cash==500000)
 assert(cczmp_licenses.debug_issue("D"));assert(cczmp_gear.buy("wpn_cczmp_pm"));assert(db.actor.cash==482000)
 assert(cczmp_gear.buy("wpn_cczmp_pm"));assert(not cczmp_gear.buy("wpn_cczmp_pm"));clock=clock+86401;assert(cczmp_gear.buy("wpn_cczmp_pm"))""",
 'organization_restrictions_and_ammo_weights':r"""skills();friendly_trader();db.actor.cash=1000000;role("cobra")
 assert(not cczmp_gear.buy("cczmp_armor_patrol"));assert(not cczmp_gear.buy("cczmp_ammo_9x19_ap"))
 assert(cczmp_gear.buy("cczmp_ammo_9x19_hp"));assert(cczmp_items.number("item_cczmp_ammo_9x19_fmj","box_size",0)==30)""",
 'regional_armor_single_reduction':r"""skills();local vest=actor_item("cczmp_armor_patrol");vest.outfit=true;vest.cond=1;db.actor.slots={[7]=vest}
 local h={type=hit.fire_wound,power=1};callbacks.actor_on_before_hit(h,2,{});assert(math.abs(h.power-.4)<.0001)
 h={type=hit.fire_wound,power=1};callbacks.actor_on_before_hit(h,1,{});assert(h.power==1)
 assert(cczmp_gear.reinforce(vest));assert(not cczmp_gear.reinforce(vest))
 h={type=hit.fire_wound,power=1};callbacks.actor_on_before_hit(h,2,{});assert(math.abs(h.power-.25)<.0001)""",
 'filter_is_equipped_and_expires_in_game_time':r"""skills();local mask=actor_item("cczmp_helmet_pmk");local filter=actor_item("cczmp_filter")
 assert(not cczmp_gear.replace_filter());db.actor.slots={[12]=mask};assert(cczmp_gear.replace_filter());assert(cczmp_gear.filtered("spores"));assert(not cczmp_gear.filtered("chemical"));assert(not db.actor:object_id(filter:id()))
 clock=clock+3600;assert(not cczmp_gear.filtered("spores"))""",
 'cooler_bonus_only_sold_artifacts':r"""skills();db.actor.cash=100;actor_item("cczmp_cooler");local art=actor_item("af_test");art.artifact=true
 callbacks.actor_on_trade(art,false,1000);assert(db.actor.cash==100)
 callbacks.actor_on_trade(art,true,1000);assert(db.actor.cash==300)
 callbacks.actor_on_trade(actor_item("weapon"),true,1000);assert(db.actor.cash==300)""",
 'non_electronic_item_cannot_consume_battery':r"""skills();local med=actor_item("cczmp_med_medkit");cczmp_items.item_state(med).charge=10;local battery=actor_item("cczmp_battery_device")
 assert(not cczmp_items.recharge(med:id()));assert(db.actor:object_id(battery:id()))"""
})

GEAR_CASES=list(CASES.values())[-6:]


RELEASE_GEAR_CASES={
 'scoped_weapon_metadata_and_device_actions':r'''skills();local sec="wpn_cczmp_mp7_acog";local item=actor_item(sec);item.weapon=true
 assert(cczmp_items.canonical(sec)=="wpn_cczmp_mp7");assert(cczmp_items.definition(sec)=="weapon")
 assert(cczmp_items.name(sec)=="cczmp_item_wpn_cczmp_mp7")
 assert(cczmp_gear.section(sec)=="wpn_cczmp_mp7")
 assert(cczmp_items.item_state(item).section==sec)
 assert(not cczmp_items.definition("wpn_cczmp_mp7_fake"))
 local c=cczmp_ui.get_ctrl();c.page="items_devices";c:refresh()
 local found=false;for _,r in ipairs(c.lines)do if r.act=="items_device:"..item:id()then found=true end end;assert(found)
 c:handle_action("items_device:"..item:id());c:refresh()
 found=false;for _,r in ipairs(c.lines)do if r.act=="items_tuning:accuracy"then found=true end end;assert(found)''',
 'AP_uses_correct_head_and_torso_previous_class':r'''skills()
 local gun=actor_item("test_gun",npc);gun.weapon=true;function gun:get_ammo_type()return 0 end;npc.active_weapon=gun
 system_ini=function()return {line_exist=function(self,s,k)return k=="ammo_class"end,r_string=function()return "cczmp_ammo_9x18_ap"end,section_exist=function()return true end}end
 local helm=actor_item("cczmp_helmet_tactical");helm.cond=1
 local vest=actor_item("cczmp_armor_plate");vest.outfit=true;vest.cond=1;db.actor.slots={[12]=helm,[7]=vest}
 local h={type=hit.fire_wound,power=1,draftsman=npc};callbacks.actor_on_before_hit(h,1,{});assert(math.abs(h.power-.5)<.0001,h.power)
 h={type=hit.fire_wound,power=1,draftsman=npc};callbacks.actor_on_before_hit(h,2,{});assert(math.abs(h.power-.4)<.0001,h.power)
 assert(cczmp_gear.reinforce(helm));h={type=hit.fire_wound,power=1,draftsman=npc};callbacks.actor_on_before_hit(h,1,{});assert(math.abs(h.power-.375)<.0001,h.power)'''
}
CASES.update(RELEASE_GEAR_CASES)
GEAR_CASES.extend(RELEASE_GEAR_CASES.values())

class Items(unittest.TestCase):
 def run_case(self,script):
  lua=LuaRuntime(unpack_returned_tuples=True)
  def convert(value):
   if isinstance(value,dict):return lua.table_from({k:convert(v) for k,v in value.items()})
   return value
  configs={}
  for rel in ['cczmp/operations.ltx','cczmp/items.ltx','cczmp/transport.ltx']+[f'cczmp/law/{n}.ltx' for n in ('uk','ak','fp','settings','constitution')]:
   p=STAGE/'gamedata/configs'/rel
   if not p.exists():p=ROOT/'gamedata/configs'/rel
   cfg=configparser.ConfigParser(interpolation=None,strict=False,inline_comment_prefixes=(';',));cfg.read(p,encoding='utf-8-sig')
   configs[rel]={s:dict(cfg[s]) for s in cfg.sections()}
  lua.globals().configs=convert(configs);lua.execute(SETUP)
  for name in ['cczmp_law','cczmp_ops','cczmp_items','cczmp_comms','cczmp_cooler','cczmp_locks','cczmp_hacking','cczmp_engineering','cczmp_licenses','cczmp_professions','cczmp_medicine','cczmp_gear','cczmp_transport','cczmp_items_ui','cczmp_ui']:
   p=STAGE/f'gamedata/scripts/{name}.script'
   if not p.exists():p=ROOT/f'gamedata/scripts/{name}.script'
   lua.globals().loadmod(name,p.read_text(encoding='utf-8'))
  lua.execute(EXTRA)
  if script in GEAR_CASES:lua.execute(GEAR_EXTRA)
  if script in TRANSPORT_CASES.values() or script==MECHANIC_CASES["tuning_cash_native_install_and_duplicate_guard"]:lua.execute(TRANSPORT_EXTRA)
  lua.execute(script)

TRANSPORT_EXTRA=r'''
local V={};V.__index=V
function V:set(x,y,z)
 if type(x)=="table"then self.x=x.x;self.y=x.y;self.z=x.z else self.x=x;self.y=y;self.z=z end
 return self
end
function V:distance_to_sqr(o)return (self.x-o.x)^2+(self.y-o.y)^2+(self.z-o.z)^2 end
function V:distance_to(o)return math.sqrt(self:distance_to_sqr(o))end
function vector()return setmetatable({x=0,y=0,z=0},V)end
function db.actor:position()return vector():set(self.x,0,0)end
function db.actor:direction()return vector():set(0,0,1)end
function db.actor:get_current_holder()return self.holder end
level.vertex_id=function(p)vertex_points=vertex_points or {};local id=#vertex_points+1;vertex_points[id]=vector():set(p);return id end
level.vertex_position=function(id)return vertex_points[id]end
function IsHeadgear(o)return o and o.helmet end
cczmp_factions.rank_count=function()return 5 end
db.storage={}
function alife_create(sec,p,lv,gv,parent)
 if spawn_fault then return nil end
 next_item=next_item+1;local id=next_item
 local o={nid=id,nname=sec.."_"..id,sec=sec,p=vector():set(p)}
 function o:id()return self.nid end
 function o:name()return self.nname end
 function o:section()return self.sec end
 function o:position()return self.p end
 local car={fuel=20,tank=40,health=1,active=true}
 function car:GetfFuel()return self.fuel end
 function car:GetfFuelTank()return self.tank end
 function car:SetfFuel(v)self.fuel=v end
 function car:GetfHealth()return self.health end
 function car:StopEngine()self.active=false end
 function o:get_car()return car end
 objects[id]=o;server[id]={};return {id=id,name=function()return o:name()end}
end
function alife()return {object=function(self,id)
 local o=objects[id]
 return o and {id=id,name=function()return o:name()end,section_name=function()return o:section()end}
 end,release=function(self,se)objects[se.id]=nil;server[se.id]=nil end}end
local original_release=alife_release
alife_release=function(obj)
 if obj.get_car then objects[obj:id()]=nil;server[obj:id()]=nil else original_release(obj)end
end
cczmp_vehicles={nearby=function()return {}end}
cczmp_professions.nearest=function(role)return role=="vehicle_dealer"and dealer_npc or nil end
dealer_npc=service(3,"civilians",0)
cczmp_transport.on_game_start()
'''
TRANSPORT_CASES={
'transport_purchase_spawn_failure_conserves_money':r'''skills();db.actor.cash=500000
spawn_fault=true;assert(not cczmp_transport.acquire("niva","buy",false));assert(db.actor.cash==500000);assert(#cczmp_transport.contracts()==0)
spawn_fault=false;assert(cczmp_transport.acquire("niva","buy",false));assert(db.actor.cash==380000);assert(#cczmp_transport.contracts()==1)
assert(not cczmp_transport.acquire("niva","buy",false));assert(db.actor.cash==380000)''',
'transport_lease_deadline_renew_and_identity':r'''skills();db.actor.cash=100000;assert(cczmp_transport.acquire("niva","rent",false))
local r=cczmp_transport.contracts()[1];assert(r.remaining==86400);clock=clock+86401;callbacks.actor_on_update()
assert(not objects[r.id]:get_car().active);assert(cczmp_transport.renew(r.uid));assert(cczmp_transport.contracts()[1].remaining==86400);assert(db.actor.cash==88000)
objects[r.id].nname="replacement";assert(#cczmp_transport.contracts()==0);assert(not cczmp_transport.renew(r.uid));assert(db.actor.cash==88000)''',
'transport_roles_debug_and_station_guards':r'''skills();role("cobra");db.actor.cash=1000000
assert(not cczmp_transport.acquire("btr","issue",false));role("mo",1);assert(not cczmp_transport.acquire("btr","issue",false))
role("mo",4);assert(cczmp_transport.acquire("btr","issue",false));assert(db.actor.cash==1000000)
DEV_DEBUG=false;assert(not cczmp_transport.acquire("niva","debug",true))
dealer_npc=nil;assert(not cczmp_transport.acquire("niva","buy",false));assert(db.actor.cash==1000000)''',
'transport_return_occupied_and_refuel_price':r'''skills();db.actor.cash=50000;assert(cczmp_transport.acquire("niva","rent",false))
local r=cczmp_transport.contracts()[1];objects[r.id].p=vector():set(1,0,0)
assert(cczmp_transport.refuel(r.uid));assert(db.actor.cash==42000);assert(objects[r.id]:get_car().fuel==40)
db.actor.holder=true;assert(not cczmp_transport.return_rental(r.uid));assert(objects[r.id]);db.actor.holder=nil
assert(cczmp_transport.return_rental(r.uid));assert(not objects[r.id]);assert(#cczmp_transport.contracts()==0)''',
'workshop_rechecks_money_and_requires_kit':r'''skills();db.actor.cash=5000;local item=actor_item("weapon");item.weapon=true;item.cond=.2
local mechanic=service(4,"sto_kanban",0)
assert(not cczmp_engineering.workshop(item:id()));local kit=actor_item("sewing_kit_b")
system_ini=function()return {line_exist=function()return true end,r_u32=function()return 20000 end}end
assert(not cczmp_engineering.workshop(item:id()));assert(db.actor:object_id(kit:id()));assert(item.cond==.2)
db.actor.cash=10000;assert(cczmp_engineering.workshop(item:id()));assert(db.actor.cash==4000 and item.cond==1)
assert(not db.actor:object_id(kit:id()));assert(not cczmp_engineering.workshop(item:id()))''',
}
CASES.update(TRANSPORT_CASES)


MECHANIC_CASES={
'jammer_ground_identity_range_and_expiry':r'''skills();role("mvd",24);assert(cczmp_licenses.debug_issue("certificate"));assert(cczmp_licenses.debug_issue("A"))
local j=actor_item("cczmp_jammer");assert(cczmp_hacking.activate_jammer(j:id()));assert(cczmp_hacking.jammed())
for i,item in ipairs(db.actor.items)do if item:id()==j:id()then table.remove(db.actor.items,i);break end end
j.owner=nil;function j:position()return npc:position()end
npc.x=40;assert(cczmp_hacking.jammed());npc.x=60;assert(not cczmp_hacking.jammed());npc.x=0
clock=clock+600;assert(not cczmp_hacking.jammed());assert(not cczmp_items.item_state(j).jammer)''',
'raw_boar_and_cooked_boar_distinct':r'''skills();math.random=function()return 1 end
cczmp_medicine.health_info();callbacks.actor_on_item_use(actor_item("meat_boar_b"));assert(not cczmp_items.world().medical.diseases.food_poison)
callbacks.actor_on_item_use(actor_item("meat_boar"));assert(cczmp_items.world().medical.diseases.food_poison)''',
'kit_unpacks_once_keeps_native_rx_gate':r'''skills();local kit=actor_item("cczmp_medkit_mchs")
assert(cczmp_gear.open_mchs(kit:id()));assert(not cczmp_gear.open_mchs(kit:id()))
assert(db.actor:object("cczmp_med_antidote")and db.actor:object("cczmp_med_strong_painkiller")and db.actor:object("cczmp_med_adrenaline"))
assert(CInventory__eat(db.actor:object("cczmp_med_adrenaline"))==false)''',
'media_requires_registered_offence_before_case_link':r'''skills();setup_target();local camera=actor_item("cczmp_media_kit")
function npc:active_item()return nil end
assert(cczmp_gear.use_special(camera:id(),key));assert(#cczmp_gear.case_recordings(key,"uk_3_1")==0)
cczmp_ops.add_incident("kidnap",key,"actor","registered incident","uk_3_1")
assert(cczmp_gear.use_special(camera:id(),key));local r=cczmp_gear.case_recordings(key,"uk_3_1");assert(#r==1)
assert(#cczmp_gear.case_recordings(key,"uk_3_3")==0)''',
'tuning_cash_native_install_and_duplicate_guard':r'''skills();db.actor.cash=9000;local gun=actor_item("wpn_cczmp_akm");gun.weapon=true
function gun:has_upgrade(k)return self.upgrades and self.upgrades[k]end
function gun:install_upgrade(k)self.upgrades=self.upgrades or {};self.upgrades[k]=true;assert(inventory_upgrades.force_upgrade)end
service(4,"sto_kanban",0);inventory_upgrades={force_upgrade=false}
assert(not cczmp_engineering.tuning(gun:id(),"accuracy"));db.actor.cash=30000
assert(cczmp_engineering.tuning(gun:id(),"accuracy"));assert(db.actor.cash==20000);assert(not inventory_upgrades.force_upgrade)
assert(not cczmp_engineering.tuning(gun:id(),"accuracy"));assert(db.actor.cash==20000)''',
}
CASES.update(MECHANIC_CASES)

for name,script in CASES.items():setattr(Items,'test_'+name,lambda self,s=script:self.run_case(s))
if __name__=='__main__':unittest.main(verbosity=2)
