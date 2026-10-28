[Русский](../../../../modules/cczmp-locks/README.md) · **English** · [Documentation index](../../docs/INDEX.md) · [Translation notes](../../TRANSLATION.md)

# CCZMP Locks - the original module and the one being tested test harness

**Project:** [STALKER X CCZMP](../../README.md) · **Base:** S.T.A.L.K.E.R. Anomaly 1.5.1 / X-Ray · **Source snapshot:** 10/09/2026 · **Control check:** 10/29/2026

> **Status: working integrated prototype / source showcase.** This is the actual CCZMP Lua code and a minimal selection of its dependencies, not pseudocode or a standalone installer. **21/21 profile regression checks** were completed in the test environment (LuaJIT 2.1 via Python/Lupa). Individual game checks with cold loading were confirmed by saved reports on 10/09/2026, but **a full native run on the current composition of the game was not carried out on 10/29/2026**.

## What is implemented

- **PIN 4–8 digits**, including leading zeros; three incorrect attempts will result in a ban for 300 game seconds.
- Temporary access **120 game seconds**. After saving loading, public access is not restored automatically.
- Up to **12 small items / 10 kg** contents; The case takes into account the weight of the cargo.
- Items move as **original ALife objects**, not as newly created copies.
- Identity control by UID/ID/name/section, fixing **pending transfers**, protection against re-extraction and repeated actions.
- Preserving item state and restoring durability after loading where native serialization does not hold it.
- Game "code master key" with charge consumption, skill requirements, game completion time and saveable task.
- The inventory/case interface is integrated into the CCZMP shell, but is not included in a separate independent application.

**Important:** this is the logic of a *fictional game* case, not a cryptographic safe. The PIN is stored in game data; authorization is designed for game mechanics, not for protecting real secrets.

## Architecture and sources

| Path | Destination |
|---|---|
| [`cczmp_locks.script`](../../../../modules/cczmp-locks/gamedata/scripts/cczmp_locks.script) | PIN, access, container, transfer, recovery and blocking |
| [`cczmp_items.script`](../../../../modules/cczmp-locks/gamedata/scripts/cczmp_items.script) | Item registry, UID, tokens, state, tasks |
| [`cczmp_ops.script`](../../../../modules/cczmp-locks/gamedata/scripts/cczmp_ops.script) | Game Time, Identities, Saved Operations |
| [`cczmp_hacking.script`](../../../../modules/cczmp-locks/gamedata/scripts/cczmp_hacking.script) | In-game autopsy operation |
| [`cczmp_items_ui.script`](../../../../modules/cczmp-locks/gamedata/scripts/cczmp_items_ui.script) | Case screen, PIN field, actions |
| [`test_locks.py`](../../../../modules/cczmp-locks/tools/items_work_20261009/test_locks.py) | 21 Directed Regression Scenarios |

In the folder `gamedata/` there are **15 associated proprietary Lua modules** and **8 configurations** - exactly the software set on which the attached stand is launched. Other subsystems are included only as bench dependencies; **not** claimed to be part of the standalone Locks release. `tools/` contains four Python test environment files.

## How to run checks

Requires Python with [Lupa](https://pypi.org/project/lupa/) installed (build with `lupa.luajit21`). From **this folder** run:

```powershell
python -m pip install lupa
python -m unittest discover -s tools/items_work_20261009 -p test_locks.py -v
```

Expected result: `Ran 21 tests ... OK`. The tests use emulation of the available Lua/X-Ray APIs and **do not run Anomaly itself**. When preparing the public version, the entry in `test_items.py` was removed from the test import: the testbed was re-run, and the SHA-256 of the test file did not change during launch. [Test protocol](TEST_REPORT.md).

## Integration into the game

**Do not copy this entire directory over your `gamedata`.** It does not contain assets, a full configuration logger, all working custom screens, or a compatible manifest for a custom build of Anomaly. To play, you need the base CCZMP mod with its initialization, items, UI and resources. Sources are needed here for auditing, testing and demonstrating engineering implementation. [Interfaces and restrictions](INTEGRATION.md).

## What has not yet been verified

- Moving the case/container between all game locations using native testing;
- removal or destruction of the container in all states and complex scenarios of item loss;
- regression check after all subsequent changes to the build on October 10–28;
- long game walkthroughs, price balance, custom 3D animations and a ready-made network mode.

**License:** copyrighted sources are published under the [root repository license](../../../../LICENSE). Components and assets of third-party projects are not included in this collection. S.T.A.L.K.E.R. and Anomaly belong to their respective copyright holders and developers.
