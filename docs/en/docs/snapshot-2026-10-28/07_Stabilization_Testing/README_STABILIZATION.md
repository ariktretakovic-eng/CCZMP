[Русский](../../../../snapshot-2026-10-28/07_%D0%A1%D1%82%D0%B0%D0%B1%D0%B8%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B8/README_STABILIZATION.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# STALKER x CCZMP - the first stage of stabilization and life of the city

Build: Anomaly 1.5.1 build 8028. Changes are installed on top of the current project, without a new game. This is the first part of S0/S1 of the general concept: window management and memory/schedule pilot for three existing employees IC.

## How to use

1. Load your save and visit the IC database at Dead City.
2. Open the terminal using the **F6** key, select **"City Life: Employees IC"**.
3. Select an employee: see his routine, hunger, fatigue, trust, discipline, sociability and recent memories.
4. Approach this employee within normal interaction distance (4 m), open his card and select **“Say hello”**. The answer will appear in the terminal message; the memory and trust will remain.
5. For the log, open **Diagnostics and Event Log**. There you can see the number of profiles, NPCs on the network, memories, input busyness and recent events.

Login via F7 and the range of existing items are retained. Documents, certificates, gadgets, radio and trunk are opened in the same ways. When one CCZMP window is opened, the remaining CCZMP windows are closed. Escape in the terminal returns to the previous page, and on the main page closes the window; documents, certificates, gadgets, radio and trunk are locked through Escape.

## NPC pilot

Employees `staff_1`, `staff_2`, `staff_3` of an existing database are used. New copies of these NPCs are not created. The remaining employees and patrols maintain the same logic.

| Parameter | First | Second | Third |
|---|---:|---:|---:|
| Discipline | 85 | 70 | 95 |
| Sociability | 55 | 80 | 35 |
| Schedule Shift | 0 h | +1 h | +2 h |
| Initial trust | 50 | 50 | 50 |
| Initial hunger | 20 | 20 | 20 |
| Initial fatigue | 15 | 15 | 15 |

Schedule of the first: **22:00–06:00 rest**, **07:00–08:00, 13:00–14:00 and 19:00–20:00 food**, the rest of the time service. The second and third schedules are shifted by one and two hours. NPCs use already proven navigation points near the base: they walk between duty and rest places using standard `beh`, and sit down during breaks and rest. This is still a vacation on the territory of the base, not a separate NPC housing.

Combat, injury, normal conversation and detention take precedence over the schedule. Once freed, the NPC returns to routine. Discipline is still a preserved profile feature; Sociability influences the response when greeting. Hunger and fatigue currently show needs and change according to a schedule: they do not consume food items and do not cause damage.

Memories:

- Greeting: trust +1, no more than once per game hour. The answer depends on sociability and trust.
- Damage from the player: trust -20, no more than one event per 10 game seconds. Repeated damage remains the game's standard damage; limited only to recording memories and changes in trust.
- Death: the death mark is saved. The life subsystem does not revive NPCs.

Trust and needs are limited to 0–100. One NPC stores the last 12 memories. There is no automatic revenge, quests, transfer of information to other NPCs and the impact of this trust on overall reputation.

## Save and load

The profiles are in the ALife state of the current save (`cczmp_items.life`), the log is in `cczmp_items.runtime`. Timers use saved game time, so after loading the old save is restored exactly to its state. There is no external state base.

The profile checks the ID, internal name and section of the object, and additionally stores the existing identity key `cczmp_ops`. When the identity key is changed, the profile is created anew even if the ID, internal name and section match. A single numeric ID match is not enough to transfer memory to another object.

During loading and the pause, the needs do not change. After loading, the needs timer starts from the first game frame: technical waiting for resources does not count as time spent by the NPC. The schedule is selected according to the current game time of the engine.

Life is updated every 2 seconds in real time. At another location, needs are calculated without moving physical models: the crossed schedule intervals are taken into account, maximum the last 24 game hours in one recalculation. This is a limited background simulation of three employees.

Game clock rates:

| Mode | Hunger per hour | Fatigue per hour |
|---|---:|---:|
| Service | +5 | +4 |
| Food | −55 | −3 |
| Holidays | +2 | −14 |

The window status is checked every 250 ms. It only unregisters CCZMP windows if the instance has disappeared or been hidden by the engine. The blocking of the regular game interface remains under the control of the standard `Unregister_UI`. The log stores the last 80 events; the screen shows the last 20.

## Files and rollback

Main new files:

- `gamedata/scripts/cczmp_runtime.script` - general window lifecycle, checking object tokens, logging and diagnostics.
- `gamedata/scripts/cczmp_life.script` - needs, memory, timers and schedule selection.
- `gamedata/scripts/cczmp_life_ui.script` - employee cards in F6.
- `gamedata/configs/cczmp/life_logic.ltx` - standard motion and animation schemes.
- `gamedata/configs/text/rus/st_cczmp_life.xml` - Russian lines, Windows-1251.

Changed the opening points of six windows and transferred control to three employees in `cczmp_deadcity.script`. Models, fuel, Mi-2 flight, radio broadcast and item storage operations are not changed by this package.

Backup copy of original modified files: `D:\CCZMP PROJECT\_backups\stabilization_s0_s1_20261012`. It contains a manifest of the source and installed hashes. When the game is closed, you can run the attached `ROLLBACK_STABILIZATION.py` through Python: it will check the hashes and restore the original files. If the files have already changed after installation, the script will refuse to overwrite them. To perform a manual rollback, restore the seven old scripts and delete the five new files listed in the manifest with `before: null`. The saved state of new subsystems itself is not executed without their scripts. If you then install the package again, the profiles will continue to work from this state.

## Border of this stage

The full concept remains a further work program. There is still no autonomous economy of the entire city, housing and rent, a new set of professions, trade chains, an online world or scaling for thousands of players. First, the small saveable NPC system on the current engine is tested. The next separate stage is the real tasks of a courier, mechanic and investigator with verifiable rewards and saving the result.
