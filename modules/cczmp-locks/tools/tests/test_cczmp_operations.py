"""Lua 5.1 backend integration regressions; native engine calls remain runtime checks."""
import configparser
from pathlib import Path
import unittest
from lupa.lua51 import LuaRuntime
ROOT=Path(__file__).resolve().parents[2]
SETUP=r'''world, storage, times, callbacks, objects, server = {}, {}, {}, {}, {}, {}
clock=10000; guild="sk"; grade=3; true_guild="actor_cczmp_sk"
function RegisterScriptCallback(k,f) callbacks[k]=f end
function printe(...) end
local npc_mt={__eq=function()error("engine objects must compare IDs")end}
function IsStalker(n) return n and n.human end
function IsWeapon(item) return item and item.weapon==true end
local pos={}
function pos:distance_to_sqr(other) return (self.x-other.x)^2 end
function make_npc(id,name,cash)
 local n={human=true,nid=id,nname=name,cash=cash,x=0,dead=false,community="civilians",org_rank=0,items={}}
 setmetatable(n,npc_mt);objects[id]=n;storage[id]={};server[id]={};db.storage[id]={object=n}
 function n:id() return self.nid end
 function n:name() return self.nname end
 function n:section() return "sim_default_cczmp" end
 function n:character_community() return self.community end
 function n:character_name() return self.nname end
 function n:alive() return not self.dead end
 function n:position() return setmetatable({x=self.x},{__index=pos}) end
 function n:money() return self.cash end
 function n:give_money(v) assert(v==math.floor(v) and self.cash+v>=0);self.cash=self.cash+v end
 function n:transfer_money(v,other) self:give_money(-v);other:give_money(v) end
 function n:wounded() return false end
 function n:critically_wounded() return false end
 function n:best_enemy() return self.enemy end
 function n:active_item() return self.gun end
 function n:weapon_strapped() return false end
 function n:inventory_for_each(fn) for _,item in ipairs(self.items) do fn(item) end end
 function n:has_info() return false end
 function n:change_goodwill(value,id) assert(id==db.actor);self.goodwill=(self.goodwill or 0)+value end
 return n
end
db={storage={}};db.actor=make_npc(0,"Actor",1000);npc=make_npc(1,"Citizen",500)
local gun={weapon=true}
function gun:section() return "wpn_test" end
function gun:id() return 100 end
db.actor.gun=gun
level={object_by_id=function(id) return objects[id] end}
function alife() return {object=function(self,id) local n=objects[id];return n and {id=id,name=function()return n:name()end} end} end
alife_storage_manager={get_se_obj_state=function(se,create)return server[se.id] end,get_state=function() return world end,get_game_object_state=function(n,create) return storage[n:id()] end}
local CT={};CT.__index=CT
function CT:diffSec(o) assert(getmetatable(o)==CT);return self.t-o.t end
game={get_game_time=function() return setmetatable({t=clock},CT) end}
function save_ctime(a,k,v) assert(getmetatable(v)==CT);times[k]=v end
function load_ctime(a,k) return times[k] end
function get_actor_true_community() return true_guild end
cczmp_factions={faction=function() return guild end,rank=function() return grade end,
 actor_community=function(id)return "actor_cczmp_"..id end,
 faction_of_object=function(n) return n:id()==db.actor:id() and guild or n.community end,
 object_rank=function(n)return n.org_rank end,set_object_rank=function(n,g) n.org_rank=g;return true end,
 is_state=function(g) return g=="sud" or g=="sk" or g=="mvd" or g=="prokuratura" end,
 is_criminal=function(g) return g=="cobra" or g=="barrikada" end,is_ally=function()return false end}
function role(g,r) guild=g;grade=r or 0;true_guild="actor_cczmp_"..g end
cczmp_custody={hold=function(n,h) assert(n:id()~=db.actor:id() and n:alive());n.held=true;return true end,
 restore=function(n,h)n.held=false;return true end,maintain=function(n,h)n.held=true end,forgotten=function()end}
function ini_file(path)
 local d=configs[path:gsub("\\","/")];assert(d,"unknown INI "..path)
 local checked,lines={},{}
 return {section_exist=function(self,s) checked[s]=true;return d[s]~=nil end,
 line_exist=function(self,s,k) assert(checked[s] and d[s]);lines[s..":"..k]=true;return d[s][k]~=nil end,
 r_string=function(self,s,k) assert(lines[s..":"..k] and d[s][k]);return d[s][k] end}
end
function loadmod(name,source)
 local env=setmetatable({},{__index=_G});_G[name]=env
 local fn=assert(loadstring(source,"@"..name));setfenv(fn,env);fn();return env
end
key=nil
function setup_target() key=cczmp_ops.person(npc);cczmp_ops.person(db.actor) end
function endorsed_case()
 role("sk",3);local ok,_,id=cczmp_ops.open_case(key,"uk_3_1");assert(ok)
 assert(cczmp_ops.statement(id,"Witness statement"));assert(cczmp_ops.submit_case(id))
 role("prokuratura");assert(cczmp_ops.endorse_case(id));role("sud",8);return id
end
'''
CASES={
"death_without_callback_cleans_hold":r'''setup_target();local id=endorsed_case();assert(cczmp_ops.issue_warrant(id,"arrest"));role("mvd",6);assert(cczmp_ops.arrest(key));npc.dead=true;cczmp_ops.actor_update();assert(not cczmp_ops.hold_info(key));assert(server[1].cczmp_identity_dead)''',

"persistent_key_offline":r'''setup_target();local id=endorsed_case();assert(cczmp_ops.issue_warrant(id,"arrest"));local oldkey=key;storage[1]={};assert(cczmp_ops.person(npc)==oldkey);role("mvd",6);assert(cczmp_ops.arrest(oldkey))''',
"npc_author_context_and_distance":r'''setup_target();local id=endorsed_case();assert(cczmp_ops.issue_warrant(id,"arrest"));local officer=make_npc(2,"Officer",0);officer.community="mvd";officer.org_rank=6
cczmp_factions.actor_community=function(g)return g=="mvd" and "mvd" or "actor_cczmp_"..g end
cczmp_civic={is_officer=function(n)return n:id()==2 end};role("cobra",0);db.actor.x=100;assert(cczmp_ops.official_call(officer,"arrest",key));assert(guild=="cobra" and grade==0);local w=world.cczmp_operations.warrants;for _,r in pairs(w)do assert(r.executor.faction=="mvd" and r.executor.person~="actor")end
assert(not cczmp_ops.official_call(npc,"arrest",key));assert(not cczmp_ops.official_call(officer,"rob",key,100));assert(not cczmp_ops.can("arrest"))''',
"npc_context_reset_after_lua_error":r'''setup_target();local officer=make_npc(2,"Officer",0);officer.community="mvd";officer.org_rank=6;cczmp_civic={is_officer=function()return true end};cczmp_factions.actor_community=function()return "mvd" end
local old=cczmp_ops.open_case;cczmp_ops.open_case=function()error("fault")end;assert(not cczmp_ops.official_call(officer,"open_case",key,"uk_3_1"));cczmp_ops.open_case=old;role("cobra");assert(not cczmp_ops.can("arrest"))''',

"court_and_prosecutor_gates":r'''setup_target();local ok,_,id=cczmp_ops.open_case(key,"uk_3_1");assert(ok)
role("sud",14);assert(not cczmp_ops.issue_warrant(id,"arrest"));role("cobra");assert(not cczmp_ops.open_case(key,"uk_3_1"))''',
"warrant_rank_and_single_execution":r'''setup_target();local id=endorsed_case();role("sud",7);assert(not cczmp_ops.issue_warrant(id,"arrest"))
role("sud",8);assert(cczmp_ops.issue_warrant(id,"arrest"));role("mvd",5);assert(not cczmp_ops.arrest(key))
role("mvd",6);assert(cczmp_ops.arrest(key));assert(npc.held);assert(not cczmp_ops.arrest(key))''',
"arrest_without_warrant_and_true_identity":r'''setup_target();role("mvd",24);assert(not cczmp_ops.arrest(key));true_guild="actor_cczmp_cobra";assert(not cczmp_ops.can("arrest"));assert(not npc.held)''',
"statement_cannot_convict":r'''setup_target();local id=endorsed_case();assert(not cczmp_ops.convict(id,0));assert(cczmp_ops.case_info(id).status=="court_review")''',
"verified_incident_and_closed_case":r'''setup_target();cczmp_ops.add_incident("kidnap",key,"actor","actual registered event","uk_3_1")
role("sk",3);local ok,_,id=cczmp_ops.open_case(key,"uk_3_1");assert(ok);assert(cczmp_ops.observe(id));assert(cczmp_ops.submit_case(id))
role("prokuratura");assert(cczmp_ops.endorse_case(id));role("sud",8);assert(cczmp_ops.convict(id,0));assert(not cczmp_ops.convict(id,0));assert(#world.cczmp_operations.people[key].convictions==1)''',
"search_single_argument_inventory":r'''setup_target();local id=endorsed_case();assert(cczmp_ops.issue_warrant(id,"search"));npc.items={npc.gun or db.actor.gun}
role("sk",3);assert(cczmp_ops.search(id));local c=cczmp_ops.case_info(id);assert(c.evidence[#c.evidence].text=="wpn_test");assert(not cczmp_ops.search(id))''',
"robbery_conserves_money_and_cooldown":r'''setup_target();role("cobra");local ok,_,amount=cczmp_ops.rob(key);assert(ok and amount==500);assert(npc:money()==0 and db.actor:money()==1500)
assert(not cczmp_ops.rob(key));role("mvd",24);assert(not cczmp_ops.rob(key))''',
"kidnap_ransom_owner_funds_release":r'''setup_target();role("cobra");assert(cczmp_ops.kidnap(key));assert(npc.held);assert(not cczmp_ops.ransom(key,501));assert(npc.held and npc.cash==500)
role("barrikada",9);assert(not cczmp_ops.ransom(key,100));role("cobra");assert(cczmp_ops.ransom(key,100));assert(not npc.held and npc.cash==400 and db.actor.cash==1100)''',
"distance_dead_reused_identity":r'''setup_target();role("cobra");npc.x=10;assert(not cczmp_ops.rob(key));npc.x=0;npc.dead=true;assert(not cczmp_ops.rob(key));npc.dead=false;npc.nname="Replacement";assert(not cczmp_ops.resolve(key,false))''',
"reload_preserves_hold_and_game_time_expiry":r'''setup_target();local id=endorsed_case();assert(cczmp_ops.issue_warrant(id,"arrest"));role("mvd",6);assert(cczmp_ops.arrest(key))
cczmp_ops.on_game_start();callbacks.on_game_load();callbacks.actor_on_update();assert(cczmp_ops.hold_info(key));clock=clock+86401;callbacks.npc_on_update(npc);assert(not npc.held and not cczmp_ops.hold_info(key))'''
}
class Operations(unittest.TestCase):
 def test_localization_line_lengths_and_permissions_labels(self):
  import xml.etree.ElementTree as E
  xml=ROOT/"gamedata/configs/text/rus/st_cczmp_operations.xml"
  self.assertLess(max(map(len,xml.read_bytes().splitlines())),1024)
  labels={x.attrib["id"] for x in E.parse(xml).getroot()}
  cfg=configparser.ConfigParser(interpolation=None);cfg.read(ROOT/"gamedata/configs/cczmp/operations.ltx")
  for section in cfg.sections():
   if cfg.has_option(section,"actions"):
    for key in cfg.get(section,"actions").split(","):self.assertIn("cczmp_ops_"+key.strip(),labels)

 def run_case(self,script):
  lua=LuaRuntime(unpack_returned_tuples=True)
  def convert(value):
   if isinstance(value,dict):return lua.table_from({k:convert(v) for k,v in value.items()})
   return value
  configs={}
  for rel in ['cczmp/operations.ltx']+[f'cczmp/law/{n}.ltx' for n in ('uk','ak','fp','settings','constitution')]:
   cfg=configparser.ConfigParser(interpolation=None,strict=False,inline_comment_prefixes=(';',))
   cfg.read(ROOT/'gamedata/configs'/rel,encoding='utf-8-sig');configs[rel]={s:dict(cfg[s]) for s in cfg.sections()}
  lua.globals().configs=convert(configs);lua.execute(SETUP)
  for name in ('cczmp_law','cczmp_ops'):
   lua.globals().loadmod(name,(ROOT/f'gamedata/scripts/{name}.script').read_text(encoding='utf-8'))
  lua.execute(script)
for name,script in CASES.items():
 setattr(Operations,'test_'+name,lambda self,s=script:self.run_case(s))
if __name__=='__main__':unittest.main()
