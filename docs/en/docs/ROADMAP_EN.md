[Русский](../../ROADMAP_RU.md) · **English** · [Documentation index](INDEX.md) · [Translation notes](../TRANSLATION.md)

# STALKER X CCZMP roadmap

Updated October 29, 2026. [Status](STATUS_EN.md) · [System register](SYSTEMS_EN.md) · [Index](INDEX.md)

This is a development plan, not a list of completed features. Details may change after testing.

| Stage | Goal | Completion criteria |
|---|---|---|
| S0 — stability | UI input handling, save/load and correct money/item transactions | A complete, reproducible regression run in the real engine |
| S1 — NPC V1, partial | Build on the minimal core for 22 existing residents: nearby behavior, supplies, social actions and load | Complete LIFE-001…018 coverage with native/mock results distinguished; reproducible loading/transitions; no duplicate NPCs or payments |
| S2 — Dead City | Connect transport, departments, services, employment and other systems in one city | End-to-end scenarios without manually editing saves |
| S3 — 3D and animations | Convert selected donor assets into functional cars, NPCs, weapons and interactive items | Every entity functions in-game, rather than merely being displayed |
| S4 — world and professions | Economy, services, property, work and public infrastructure | Coherent workflows rather than isolated demonstrations |
| S5 — multiplayer research | Separate server prototype, authority model, storage, replication and security | A minimal secure end-to-end network prototype |
| S6 — scaling | Load testing and gradual player-count increases | Measured throughput, without assuming 1,000–2,000-player capacity in advance |

**Core principle:** stabilize the single-player world before the online stage. The target of 1,000–2,000 players must not be presented as achieved performance.

## Next verifiable results

1. Reproduce and explain the access violation. Complete ordinary and extended V1 save/load transitions, and separately investigate the October 22 vehicle warm-load crash. Two successful repeats do not cover the entire test matrix.
2. Refine the 22-resident minimal core: nearby physical behavior for the remaining citizens, finite food supplies, reactions to an empty treasury, work interruptions and transitions. Full GOAP and families remain separate work.
3. Test each new vehicle section for driving, passengers/services, persistence and collisions; separately define the limits of aircraft and rail prototypes.
4. Run integration regression for UI, documents, items and banking after all new packages. Use the Locks mock harness as an additional check alongside in-game tests.
5. Maintain summaries and indexes following the [maintenance guide](INDEXING_EN.md). Retain dated reports and explicitly identify new evidence.

First-wave priorities are UI/Lua stability, save/load, physical vehicles, a correct 3D pipeline and first-/third-person document animations. Task discussions can start from public guides and a small non-commercial proof of concept, without distributing the full gamedata.
