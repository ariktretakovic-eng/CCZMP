[Русский](../../../../modules/cczmp-locks/TEST_REPORT.md) · **English** · [Documentation index](../../docs/INDEX.md) · [Translation notes](../../TRANSLATION.md)

# CCZMP Locks - recheck protocol

**Date:** October 29, 2026. **Code source:** tested package 10/09/2026, selected sources and fixtures from `locks_stage`.

## Execution

- A **temporary copy** of the project has been created; main `gamedata`, game saves and settings have not been changed.
- Selected exactly **27 files** (15 Lua, 8 LTX, 4 Python); models, textures, zip archives and private game data are not required for testing.
- Test import changed to **not overwrite** `test_items.py` during startup; rerun after this change is successful.
- Lupa version on the test machine: **2.8**; test runtime - `lupa.luajit21`.

```text
python -m unittest discover -s tools/items_work_20261009 -p test_locks.py
.....................
----------------------------------------------------------------------
Ran 21 tests in 1.272s

OK
HARNESS_INTEGRITY unchanged=True exit=0
```

## What is covered

PIN format and leading zeros, limit of incorrect attempts, timers, reset of open access at loading, capacity and weight, prohibitions on nested cases and equipment, identity of original cargo, refusal/delay of transfer, no copying of items, saving incomplete transfer, saving and restoring durability, canceling/completion of hacking, charge consumption and UI reaction.

## Separate native check (historical)

The saved report dated 10/09/2026 recorded the opening/closing of the case, the input interface, the transfer of the real item, the initial strength **0.73**, as well as **cold loading** with the restoration of the original object and the unfinished task. Source: [stabilization report](../../docs/snapshot-2026-10-28/07_Stabilization_Testing/README_STABILIZATION.md) and [historical description of Locks](../../docs/snapshot-2026-10-28/03_Items_Gadgets_Mechanics/LOCKS_NEXT.md).

This is **not** a new playtest on 10/29/2026 and does not confirm compatibility with all future versions of the mod.

**Limitations:** The engine emulator does not replace a physical game run; transition between locations and all scenarios with loss of ALife objects are not closed.
