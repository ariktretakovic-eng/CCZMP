[Русский](../../../../snapshot-2026-10-28/13_Autonomous_Life_V1/ROLLBACK.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Safe shutdown and rollback

1. Close the game. Save a separate copy of the current `appdata/savedgames`.
2. The softest option: install `enabled=false` in `gamedata/configs/cczmp/life_v1.ltx`. Restart the game. Data is not erased; the original mechanics and old profiles IC remain.
3. To perform an exact rollback, check:

   `python "D:\CCZMP PROJECT\tools\autonomous_life_v1\rollback.py"`

4. Only after successful verification apply:

   `python "D:\CCZMP PROJECT\tools\autonomous_life_v1\rollback.py" --apply`

The script compares each current file with the final `installed.json`. If someone else changes or the file is missing, it stops working until the first record. Then it restores the old files from `tools/autonomous_life_v1/baseline` and deletes only the unmodified new files from this stage. Old packages of October 18/19/22 are not rolled over the project. User saves and settings are not changed.

Additional data in a save after deleting a module is not automatically deleted. Don't reset the whole world and don't erase ALife for cleaning. Unique real payments already made and items eaten are the consequences of the saved world; file rollback does not return money and food retroactively. To return to the state before installation, you need your own previous slot.

Test `zzzz_cczmp_life_owned.script` should not be in the release composition. A reproducible copy of it is in tools, and execution is limited to a separate native_appdata. Test profiles do not replace player appdata.
