[Русский](../../../../snapshot-2026-10-28/07_%D0%A1%D1%82%D0%B0%D0%B1%D0%B8%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B8/stabilization_work_20261012__TEST_REPORT.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Check the first stage S0/S1

## Local checks Lua 5.1

Ten tests passed:

1. Syntax of all new and changed scripts.
2. Removing legacy CCZMP registration while keeping the foreign window blocked.
3. Window exclusivity: a new window closes the previous one.
4. Limit the log to the last 80 events.
5. Replacing an object with the same ID and a different name does not inherit memory.
6. A new identity key with the same ID, name and section also does not inherit memory.
7. Schedule with shifts, calculation of needs when crossing several intervals.
8. Limit greetings to one game hour and prioritize detention over scheduling.
9. Only the player's damage changes the memory of attacks; memory is limited to 12 events.
10. loading and pause do not consume saved needs, even if the engine's game timer continues to run.

Playback file: `tools/tests/test_stabilization.py`; dependency - `lupa` with Lua 5.1. For installed `lupa` you can run from the root of the package; The built-in path in the test is intended for the development environment.

## Checking in the engine

The final warm launch has passed: three existing NPCs are connected to the system and remain alive/online, the greeting is recorded once, the document is switched to the ID and closed using Escape, F6 opens the terminal, the hidden window automatically unregisters itself. Passed the transitions radio → gadget → help → document → terminal, opening two real trunk inventories, physical F7 and Escape, employee transition to night rest and save record. The launch took 203.34 s, including loading. After exiting, user save hashes were checked and settings were restored.

In the first cold start, personality, trust and memory were restored, but the consumption of needs exceeded the tolerance. The diagnostic run confirmed: the numbers themselves are loaded accurately, but by the time `on_game_load` the engine clock has time to pass 608 game seconds at `precache_frame=58`. Added stopping the calculation of needs at loading/pause with the timer relocating to the first game frame. The tenth local check reproduces this case. The final cold loading of the corrected version took place in the new game process (169.19 s including loading). Identity `p222`, object token, trust 51 and one memory restored. Hunger: 12.45342 → 12.46685; fatigue: 23.17595 → 23.08192 - changes correspond to the short time of a normal game after loading, without the cost of technical waiting for resources. The standard rest scheme has been restored; F6 displays three cards and diagnostics. The interface was examined using a snapshot of a real game window: Russian lines are readable, the list and buttons fit.

The final hash check confirmed 12 installed files. The temporary test script has been removed. The original user saves are not changed, the settings are restored byte by byte. No new game needed. Two preliminary runs stopped on errors in the test script: the card was opened before selecting an employee, then they mistakenly tried to get a local GUI variable of the regular debugger as a public field. In both cases, the game ended normally and hash control confirmed the safety of the original user saves and settings. These errors are corrected in the verification script.
