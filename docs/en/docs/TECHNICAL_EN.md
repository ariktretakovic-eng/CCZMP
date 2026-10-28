[Русский](../../TECHNICAL_RU.md) · **English** · [Documentation index](INDEX.md) · [Translation notes](../TRANSLATION.md)

# Technical overview for developers

Updated 10/29/2026. [Status](STATUS_EN.md) · [Systems](SYSTEMS_EN.md) · [Index](INDEX.md)

## Stack and scope

- Game: S.T.A.L.K.E.R. Anomaly 1.5.1, Monolith/X-Ray; current work is carried out offline.
- Game logic: Lua 5.1 / LuaJIT-like X-Ray environment, LTX configs, XML interfaces.
- 3D: Blender with Blender X-Ray tools; OGF/OMF/OBJECT, DDS formats.
- Localization: Russian game XML must preserve the correct **Windows-1251**, and not be arbitrarily converted to UTF-8.
- State: subsystem data persists in ALife/world storage and game saves. Check for NPC replacement when numeric IDs are reused.

## Subsystems and work areas

| Direction | Internal entry points (landmarks) | Upcoming tasks |
|---|---|---|
| UI/diagnostics | `cczmp_ui.script`, `cczmp_runtime.script` | Esc/F6/F7, window registration, control return, compatibility |
| NPC Simulation | `cczmp_life_core/bridge/events/economy/careers/social.script`, `life_v1.ltx`; old adapter `cczmp_life.script` | 22 existing residents; general acceptance testing loads, nearby behavior, supply and expansion of autonomy |
| Law/organizations | `cczmp_ops.script`, `cczmp_civic.script`, `cczmp_factions.script` | Authority, evidence, correct consequences and preservation |
| Documents | `cczmp_documents.script`, `cczmp_documents_ui.script` | 1P/3P Animation, UI Lifecycle, document-issuance checks |
| Transport | `cczmp_vehicles.script`, `cczmp_taxi*.script` | Physics, passengers, navigation, cold reload |
| Radio | `cczmp_radio.script`, `cczmp_broadcast.script` | Continuity, synchronization, separate audio sources |
| Items | `cczmp_items.script`, `cczmp_hacking.script`, `cczmp_engineering.script` | Consistent save/load, no duplication, real interactions |
| Donors | `cczmp_donors.script`, Blender/X-Ray converters | Separation of static props and real items/NPC/CCar/weapons |

These names describe the working build; its full composition is not published here. The open repository contains separately the early fragment `gamedata/` and the [original Locks module](../modules/cczmp-locks/README.md) with its test-harness dependencies. You should not mix their versions or consider the modules directory to be the installation package of the entire game. The full list of public files is [FILES.json](../../FILES.json).

## Engineering quality criteria

1. **No hidden side-effects.** Closing the custom UI does not break inventory, pause, dialogue, F6/F7 and further interactions.
2. **Persistent saves.** One NPC does not inherit the memory of another when reusing a numeric ID; the state is rolled back at loading of the earlier save.
3. **No duplication.** Banking transactions, services, items and taxis do not write off/re-issue resources when double-clicking or restoring.
4. **native in-game checks.** A successful syntax or mocked Lua test does not replace the actual X-Ray test.
5. **Performance.** First small pilots with measurement, then scaling; heavy OGFs require LOD and optimization.
6. **Data Security.** Screenshots, logs and replays are cleared of personal information, tokens, absolute user paths and assets with an unclear license.

## Tests that are already documented

- Historical pilot S0/S1: 10 local checks of Lua 5.1, native warm and cold start; tested three NPCs, saving and transitions of interfaces. Measurements from a local report, not independent external QA.
- W140: single scenario AnomalyDX9AVX with real controls, exiting the car and re-reading fuel.
- Donor resources: checking 202 file sets, not acceptance testing 202 full-fledged game objects.
- Taxi: physical trip with a passenger ~80 meters; incomplete coverage of edge cases.

- Autonomous Life V1: [native matrix LIFE-001...018](snapshot-2026-10-28/13_Autonomous_Life_V1/TEST_REPORT.md), 22 residents, 10 game days outside the location, real ledger transactions and food consumption, cold loading and return of the same objects. Full V1 is not accepted.
- [Warm-load V1](snapshot-2026-10-28/13_Autonomous_Life_V1/WARM_LOAD.md): primary AV, control without kernel, two normal retries after precache protection; the extended transition script is not accepted. Transport defect 22.10 is not closed.
- [Performance V1](snapshot-2026-10-28/13_Autonomous_Life_V1/PERFORMANCE.md): 100/1000/5000 logical NPCs under mock/LuaJIT, not native FPS and not proof of support for that many physical inhabitants.
- [CCZMP Locks](../modules/cczmp-locks/TEST_REPORT.md): sources 09.10, 21/21 directed mock regressions re-passed 29.10. This documentation update does not replicate game QA.

## Integration contracts V1

[Detailed APIs and data owners](snapshot-2026-10-28/13_Autonomous_Life_V1/API_CONTRACTS.md): `cczmp_ops.person` specifies the UID; `cczmp_bank.move_once` posts existing money with a transaction receipt; The new simulator uses ALife storage rather than second balance or respawning of residents. The queue is limited by budget, an unsuccessful event is quarantined. [Options](snapshot-2026-10-28/13_Autonomous_Life_V1/CONFIG.md), [file composition](snapshot-2026-10-28/13_Autonomous_Life_V1/FILES.md), [rollback](snapshot-2026-10-28/13_Autonomous_Life_V1/ROLLBACK.md).

## What is required from a new developer

Brief portfolio or public code, experience with X-Ray/Anomaly or a similar C++/Lua/3D stack; then discussing a narrow problem and accessing only a minimal reproducible example. Entry is voluntary, without guaranteed payment and a mandatory schedule. There is no need to send the entire gamedata catalog for initial acquaintance.
