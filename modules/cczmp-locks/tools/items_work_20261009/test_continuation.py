from pathlib import Path
import unittest
import test_items as T
P=Path(__file__).resolve().parent
# Run the same real Lua modules and baseline engine fixtures as the existing suite.

PRE=r'''
skills();setup_target();db.actor.cash=100000
local phone=actor_item("cczmp_phone_basic");local target_phone=actor_item("cczmp_phone_basic",npc)
assert(cczmp_comms.register_phone(target_phone,npc,true))
actor_item("cczmp_sim_module");assert(cczmp_comms.install_sim(phone:id()))
local number=cczmp_items.item_state(target_phone).sim
'''
CASES={
'phone_real_delivery_and_plan_quota':PRE+r'''
assert(not cczmp_comms.send(phone:id(),number,"hello"));assert(cczmp_comms.subscribe(phone:id(),"basic"));assert(db.actor.cash==99700)
assert(cczmp_comms.send(phone:id(),number,"hello"));assert(cczmp_items.item_state(target_phone).inbox[1].text=="hello")
assert(cczmp_comms.outbox(phone:id())[1].to==number);assert(cczmp_comms.plan_info(phone).messages==99)
assert(cczmp_items.item_state(phone).charge==99 and cczmp_items.item_state(target_phone).charge==99)
assert(cczmp_comms.call(phone:id(),number));assert(cczmp_comms.plan_info(phone).calls==19)
''',
'phone_expiry_and_no_side_effects':PRE+r'''
assert(cczmp_comms.subscribe(phone:id(),"basic"));clock=clock+604800
assert(not cczmp_comms.send(phone:id(),number,"hello"));assert(cczmp_items.item_state(phone).charge==100)
assert(not cczmp_items.item_state(target_phone).inbox)
''',
'phone_limits_invalid_recipient_and_reused_ID':PRE+r'''
assert(cczmp_comms.subscribe(phone:id(),"basic"));assert(not cczmp_comms.send(phone:id(),number,""))
assert(not cczmp_comms.send(phone:id(),number,string.rep("a",141)));assert(not cczmp_comms.send(phone:id(),"unknown","hello"))
target_phone.nname="replacement";assert(not cczmp_comms.send(phone:id(),number,"hello"))
assert(cczmp_comms.plan_info(phone).messages==100)
''',
'phone_ghost_data_and_interception_permission':PRE+r'''
local sdr=actor_item("cczmp_sdr");assert(cczmp_comms.subscribe(phone:id(),"basic"))
cczmp_items.item_state(phone).os="ghost";assert(cczmp_comms.send(phone:id(),number,"secret"))
assert(cczmp_items.item_state(target_phone).inbox[1].encrypted)
role("mvd",24);assert(not cczmp_comms.intercept(number));role("schs",24)
local ok,msg,data=cczmp_comms.intercept(number);assert(ok,msg);assert(#data==0)
cczmp_items.item_state(phone).os="civil";assert(cczmp_comms.send(phone:id(),number,"public"))
ok,msg,data=cczmp_comms.intercept(number);assert(ok and #data==1 and data[1].text=="public")
cczmp_items.item_state(target_phone).os="ghost";assert(not cczmp_comms.intercept(number))
''',
'phone_physical_identity_and_unique_SIM':PRE+r'''
assert(not cczmp_comms.install_sim(phone:id()));assert(not db.actor:object("cczmp_sim_module"))
local other=actor_item("cczmp_phone_basic");actor_item("cczmp_sim_module");assert(cczmp_comms.install_sim(other:id()))
assert(cczmp_items.item_state(other).sim~=cczmp_items.item_state(phone).sim)
''',
'multiboot_installed_only_and_role_revocation':r'''
skills();local p=actor_item("cczmp_laptop_multi");actor_item("cczmp_usb_os");actor_item("cczmp_os_linux")
assert(not cczmp_items.switch_os(p:id(),"linux"));assert(cczmp_hacking.start("os_laptop",p:id()));assert(complete(true))
assert(cczmp_items.switch_os(p:id(),"civil"));assert(cczmp_items.switch_os(p:id(),"linux"));assert(not db.actor:object("cczmp_os_linux"))
local s=cczmp_items.item_state(p);s.installed_oses.government=true;role("mvd",24);assert(cczmp_items.switch_os(p:id(),"government"))
role("cobra");assert(cczmp_items.switch_os(p:id(),"civil"));assert(not cczmp_items.switch_os(p:id(),"government"))
''',
'multiboot_legacy_migration_and_fixed_guard':r'''
skills();local p=actor_item("cczmp_laptop_multi");local s=cczmp_items.item_state(p);s.os="linux";s.installed_oses=nil
assert(cczmp_items.item_state(p).installed_oses.linux);assert(cczmp_items.switch_os(p:id(),"civil"))
local q=actor_item("cczmp_laptop_basic");assert(not cczmp_items.switch_os(q:id(),"civil"))
''',
'SDR_recharge_and_signals_are_phone_metadata':PRE+r'''
local sdr=actor_item("cczmp_sdr");cczmp_items.item_state(sdr).charge=0;actor_item("cczmp_battery_device");assert(cczmp_items.recharge(sdr:id()))
assert(cczmp_hacking.start("signals",sdr:id()));assert(complete(true))
local r=cczmp_items.world().signal_report;assert(#r==1 and r[1].number==number and not r[1].text)
''',
'critical_patient_defib_power_role_and_cooldown':r'''
skills();setup_target();local d=actor_item("cczmp_defibrillator");npc.health=.1
assert(not cczmp_medicine.defibrillate(d:id(),key));role("mchs",1)
assert(cczmp_medicine.defibrillate(d:id(),key));assert(npc.health==.35 and cczmp_items.item_state(d).charge==75)
npc.health=.1;assert(not cczmp_medicine.defibrillate(d:id(),key));clock=clock+120
assert(cczmp_medicine.defibrillate(d:id(),key));npc.dead=true;assert(not cczmp_medicine.defibrillate(d:id(),key))
''',
'defib_catalog_access_and_cost':r'''
skills();cczmp_factions.get_type=function()return "neutral"end
local n=service(3,"civilians",0);cczmp_items.nearest_trader=function()return n end;db.actor.cash=100000
role("cobra");assert(not cczmp_gear.buy("cczmp_defibrillator"));assert(db.actor.cash==100000)
role("minzdrav",1);assert(cczmp_gear.buy("cczmp_defibrillator"));assert(db.actor.cash==55000)
''',
'tourniquet_time_removal_gangrene_and_surgeon':r'''
skills();db.actor.bleeding=.5;local t=actor_item("cczmp_med_tourniquet");assert(cczmp_medicine.allowed(t));callbacks.actor_on_item_use(t)
assert(cczmp_medicine.health_info().tourniquet);assert(db.actor.bleeding==0);assert(not cczmp_medicine.allowed(actor_item("jgut")))
clock=clock+179;assert(cczmp_medicine.remove_tourniquet());assert(not cczmp_items.world().medical.diseases.gangrene)
assert(db.actor.bleeding==.5);callbacks.actor_on_item_use(actor_item("cczmp_med_tourniquet"));clock=clock+180
assert(cczmp_medicine.remove_tourniquet());assert(cczmp_items.world().medical.diseases.gangrene)
local doctor=service(3,"minzdrav",2);cczmp_professions.nearest=function(r)return r=="doctor"and doctor end
assert(not cczmp_medicine.hospital());cczmp_professions.nearest=function(r)return (r=="doctor"or r=="field_surgeon")and doctor end
assert(cczmp_medicine.hospital());assert(not cczmp_items.world().medical.diseases.gangrene)
''',
'communications_UI_input_back_and_messages':PRE+r'''
local c=cczmp_ui.get_ctrl();c.items_selected=phone:id();c:handle_action("items_contact:"..number);c:refresh();assert(c.page=="items_contact")
c:handle_action("items_write");c:refresh();assert(c.page=="items_message_prompt");assert(cczmp_items_ui.is_prompt(c.page))
c.input="hello";assert(c:handle_action("items_send")=="cczmp_comms_expired");assert(c.page=="items_message_prompt")
assert(cczmp_comms.subscribe(phone:id(),"basic"));assert(c:handle_action("items_send")=="cczmp_comms_delivered");assert(c.page=="items_contact")
c:back();assert(c.page=="items_contacts");c:back();assert(c.page=="items_device")
''',
}

CASES.update({
'engineer_diagnostic_and_recycling_atomicity':r"""skills();local p=actor_item("cczmp_laptop_multi");assert(not cczmp_engineering.diagnose(p:id()))
actor_item("cczmp_multimeter");assert(cczmp_engineering.diagnose(p:id()));assert(cczmp_items.world().diagnostic.charge==100)
assert(not cczmp_engineering.salvage(p:id()));actor_item("cczmp_precision_screwdrivers")
spawn_fault=true;assert(not cczmp_engineering.salvage(p:id()));assert(cczmp_items.owned(p:id()))
spawn_fault=false;assert(cczmp_engineering.salvage(p:id()));assert(not cczmp_items.owned(p:id()))
assert(db.actor:object("cczmp_copper_wire")and db.actor:object("cczmp_components"));assert(not cczmp_engineering.salvage(p:id()))""",
'visible_weapon_license_no_hidden_inventory_search':r"""skills();setup_target();role("sk",24)
local gun=actor_item("wpn_cczmp_pm",npc);gun.weapon=true
function npc:active_item()return self.active_weapon end;function npc:weapon_strapped()return false end
assert(not cczmp_licenses.visible_violation(npc));npc.active_weapon=gun
local v=cczmp_licenses.visible_violation(npc);assert(v and v.category=="D"and v.offence=="ak_items_carry")
assert(cczmp_ops.inspect_carry(key));assert(not cczmp_ops.inspect_carry(key))
local count=0;for _,e in pairs(cczmp_ops.service_state().incidents)do if e.offence=="ak_items_carry"then count=count+1 end end;assert(count==1)
local ok,msg,id=cczmp_ops.open_case(key,"ak_items_carry");assert(ok,msg);assert(cczmp_ops.observe(id))
local case=cczmp_ops.service_state().cases[tostring(id)];assert(#case.evidence>=1)
assert(cczmp_ops.sentence_preview("ak_items_carry",0).fine==20000)
assert(not cczmp_ops.search(id))""",
'visible_weapon_registered_license_and_A_category':r"""skills();setup_target();role("sk",24)
local gun=actor_item("wpn_cczmp_sv98",npc);gun.weapon=true
function npc:active_item()return gun end;function npc:weapon_strapped()return false end
assert(cczmp_licenses.visible_violation(npc).offence=="uk_11_2")
local permit=actor_item("cczmp_license_a",npc);local p={uid=999,name=permit:name(),owner=key,category="A"}
server[permit:id()].cczmp_license=p;cczmp_items.world().licenses={records={}};cczmp_items.world().licenses.records["999"]=p
assert(not cczmp_licenses.visible_violation(npc));p.revoked=true;assert(cczmp_licenses.visible_violation(npc))
role("cobra");assert(not cczmp_ops.inspect_carry(key))""",
'phone_inbox_bounded_and_ghost_scan_anonymous':PRE+r"""
assert(cczmp_comms.subscribe(phone:id(),"basic"));for i=1,30 do assert(cczmp_comms.send(phone:id(),number,"message "..i))end
assert(#cczmp_items.item_state(target_phone).inbox==25);assert(#cczmp_comms.outbox(phone:id())==25)
cczmp_items.item_state(target_phone).os="ghost";local scan=cczmp_comms.scan();assert(scan[1].encrypted and not scan[1].key and scan[1].name~="Citizen")
""",
})
TRANSPORT_NEW={
'canonical_missing_assets_never_spawn_or_charge':r"""skills();db.actor.cash=2000000
local count=0;for _,v in ipairs(cczmp_transport.catalog())do if not v.available then count=count+1 end end;assert(count==11)
for _,id in ipairs({"lc100","ka226","gelik"})do
 assert(not cczmp_transport.acquire(id,"buy",false));assert(not cczmp_transport.acquire(id,"rent",false));assert(not cczmp_transport.acquire(id,"debug",true))
end
assert(db.actor.cash==2000000 and #cczmp_transport.contracts()==0)
""",

'GPS_purchase_marker_and_immobilizer_persisted':r"""skills();db.actor.cash=20000;assert(cczmp_transport.acquire("niva","debug",true))
local r=cczmp_transport.contracts()[1];local obj=objects[r.id];obj.p=vector():set(1,0,0);local car=obj:get_car()
function car:IsActiveEngine()return self.active end;function car:HandBreak()self.brake=true end;function car:ReleaseHandBreak()self.brake=false end
assert(not cczmp_transport.install(r.uid,"gps"));car:StopEngine();local mop=dealer_npc;dealer_npc=nil;assert(not cczmp_transport.install(r.uid,"gps"))
dealer_npc=mop;assert(cczmp_transport.install(r.uid,"gps"));assert(db.actor.cash==14000);assert(not cczmp_transport.install(r.uid,"gps"))
assert(cczmp_transport.install(r.uid,"alarm"));assert(db.actor.cash==6000)
assert(cczmp_transport.toggle_lock(r.uid));assert(car.brake and not car.active)
local spot=false;level.map_has_object_spot=function()return spot and 1 or 0 end
level.map_add_object_spot=function()spot=true end;level.map_remove_object_spot=function()spot=false end
frame=1000;callbacks.actor_on_update();assert(spot)
assert(cczmp_transport.toggle_lock(r.uid));assert(not car.brake)
""",
}
CASES.update(TRANSPORT_NEW);T.TRANSPORT_CASES.update(TRANSPORT_NEW)
COOLER_PRE=r"""
skills();IsArtefact=function(x)return x and x.artifact end;local cooler=actor_item("cczmp_cooler");function cooler:set_weight(v)self.mass=v end
system_ini=function()return {line_exist=function()return true end,r_float=function()return 2 end}end
local box={nid=5000,nname="hidden_box_original",items={}}
function box:id()return self.nid end;function box:name()return self.nname end
objects[5000]=box;server[5000]={}
function alife()return {object=function(self,id)local o=objects[id];return o and {id=id,name=function()return o:name()end,section_name=function()return id==5000 and "hidden_box"or o:section()end}end,
 set_switch_online=function()end,set_switch_offline=function()end}end
local s=cczmp_items.item_state(cooler);s.container={id=5000,name=box:name(),level="test_level",contents={}}
function transfer(from,item,to)
 for i,t in ipairs(from.items)do if t==item then table.remove(from.items,i);break end end
 to.items[#to.items+1]=item;item.owner=to
end
function db.actor:transfer_item(item,to)transfer(self,item,to)end
function box:transfer_item(item,to)transfer(self,item,to)end
function artifact()
 local art=actor_item("af_test");art.artifact=true;art.cond=.73;art.researched=true
 function art:weight()return .5 end
 return art
end
"""
CASES.update({
'cooler_original_identity_condition_capacity_and_weight':COOLER_PRE+r"""
local a=artifact();local b=artifact();local c=artifact();assert(cczmp_cooler.store(cooler:id(),a:id()));assert(cczmp_cooler.store(cooler:id(),b:id()))
assert(not cczmp_cooler.store(cooler:id(),c:id()));assert(cooler.mass==3);assert(#cczmp_cooler.contents(cooler:id())==2)
assert(cczmp_cooler.take(cooler:id(),a:id()));assert(db.actor:object_id(a:id())==a and a.cond==.73 and a.researched)
assert(cooler.mass==2.5);assert(not cczmp_cooler.take(cooler:id(),a:id()))
""",
'cooler_reused_box_identity_does_not_copy_contents':COOLER_PRE+r"""
local a=artifact();assert(cczmp_cooler.store(cooler:id(),a:id()));box.nname="replacement"
assert(not cczmp_cooler.take(cooler:id(),a:id()));assert(not cczmp_cooler.store(cooler:id(),artifact():id()));assert(#db.actor.items==2)
""",
})

CASES['road_sign_permission_failed_spawn_and_single_collection']=r"""
skills();cczmp_factions.get_type=function()return "state"end;role("mvd",24);local sign=actor_item("cczmp_road_sign")
local original_spawn=cczmp_items.spawn;local made=0
cczmp_items.spawn=function(section)
 if spawn_fault then return false,"failed" end
 made=made+1;local o=actor_item(section)
 if section=="cczmp_road_sign_placed"then
  o.owner=nil;for i,v in ipairs(db.actor.items)do if v==o then table.remove(db.actor.items,i);break end end
  function o:position()return db.actor:position()end
  local w=cczmp_items.world();w.stations[tostring(o:id())]={id=o:id(),name=o:name(),section=section,level=level.name()}
 end
 return true,"ok",o:id()
end
spawn_fault=true;assert(not cczmp_engineering.deploy_sign(sign:id()));assert(cczmp_items.owned(sign:id()))
spawn_fault=false;role("cobra");assert(not cczmp_engineering.deploy_sign(sign:id()));assert(made==0)
role("mvd",24);assert(cczmp_engineering.deploy_sign(sign:id()));assert(not cczmp_items.owned(sign:id()))
local id;for _,r in pairs(cczmp_items.world().stations)do id=r.id end;assert(id)
alife_release=function(o)objects[o:id()]=nil;server[o:id()]=nil end
assert(cczmp_engineering.collect_sign(id));assert(not cczmp_engineering.collect_sign(id));assert(made==2)
"""

class Continuation(T.Items):pass
# Don't inherit baseline tests twice in this suite.
for name in dir(T.Items):
 if name.startswith('test_'):setattr(Continuation,name,None)
for name,script in CASES.items():setattr(Continuation,'test_'+name,lambda self,s=script:self.run_case(s))
if __name__=='__main__':unittest.main(verbosity=2)
