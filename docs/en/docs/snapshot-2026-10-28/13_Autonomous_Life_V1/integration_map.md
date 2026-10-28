[Русский](../../../../snapshot-2026-10-28/13_Autonomous_Life_V1/integration_map.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Autonomous Life V1 — confirmed integration map, 28 October 2026

Working source: D:\CCZMP PROJECT. This is a staged vertical slice, not a claim of completed V1.

* `cczmp_ops.person(npc)` owns person UIDs p<serial>; `target_info(uid)` is a detached query. UID is stored on the ALife server entity (`cczmp_person_key`, name, section). No new person namespace or spawn.
* `cczmp_items.world()` uses `alife_storage_manager.get_state().cczmp_items`. Additive `autonomous_life` schema v1 contains primitives only. Original `life` profiles are preserved.
* `cczmp_bank.account_state(uid)`, `transfer(source,target,amount)` own balances. Account initialization transfers 60% of an online NPC's real cash. Add `move_once` inside bank for an atomic, receipted movement, including the existing operations treasury. No simulator balance.
* No existing wage API was found. New wage contracts live in the existing `cczmp_ops.service_state().contracts`, namespaced `life:<person>`. Treasury-funded contracts do not create budget; insufficient funds retain an earned obligation. Private employment debits an existing citizen account.
* `cczmp_factions.set_object_rank`, `object_rank`, `rank_count` own ranks. Offline adapter changes the same verified server fields and operations identity record. It does not change native community or override specialist `cczmp_profession`.
* `cczmp_deadcity.state().objects` and `cczmp_crime.state().roster` contain existing residents. Stable source keys discover them without spawning. Loaded identities register while online; registered residents then continue off-level.
* `cczmp_life.script` keeps its existing native `beh` schemes, UI, greetings and hit callbacks. A narrow guard yields needs calculation to the new module for migrated people. No patch to actor/bind_stalker/xr_logic.
* `game.get_game_time():diffSec(saved_ctime)` is the game-time clock. Loading/precache is excluded; sleeping and time advancement in gameplay generate budgeted catch-up. Electronics seconds are real play seconds and are not suitable for life time.
* `actor_on_update`, `save_state`, `on_game_load`, `npc_on_death_callback` are confirmed callback names. `axr_main` discovers on_game_start modules automatically.
* `cczmp_runtime.resolve(token)` validates ALife ID, name and section. Add UID validation before use. Online objects are re-resolved, never retained. `alife_release` removes real food from existing inventory; food references require parent ID validation and a reservation.
* `cczmp_ops.hold_info` and response marker `cczmp_response_unit` reserve official tasks. Life does not replace 111, taxi, custody, combat, or investigations.

Protected: user appdata save files and user.ltx (47 hashes), existing ALife IDs, passports, transport, mission NPCs. Original transport warm-load 0xC0000005 is still unresolved.

Before game-script changes: 140 files copied to tools/autonomous_life_v1/baseline; SHA256 baseline.json and protected.json. All installation patches must verify baseline SHA256. Tests use a separate appdata profile and existing copied test seed. A strictly profile-scoped test fixture is temporary and must be removed before final delivery.
