[Русский](../../../../snapshot-2026-10-28/04_%D0%A2%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82_%D0%B1%D1%80%D0%BE%D0%BD%D0%B5%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0_%D0%B0%D0%B2%D0%B8%D0%B0%D1%86%D0%B8%D1%8F/vehicles_work__HANDOFF_RU.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Result of autonomous donor processing (10/13/2026)

> Historical note about the first two pilots. The current status of all 202 donors is given in the “Mass Donor Integration” section below.

## Confirmed result
The tools\donors directory was checked: 202 ZIP archives were found, glTF was found in each.
Two pilots processed and installed:
- Colt M4A1 from D_U, CC-BY-4.0 - static OGF prop, non-firing weapon.
- Volkswagen van T6 from IrisProcess, CC-BY-4.0 - static black OGF props with tinted windows.

For both models, OGF is re-imported into Blender; for VW, 51 meshes and all 9 texture links have been tested. The game config has spawn sections:
- cczmp_prop_colt_m4a1 — g_spawn cczmp_prop_colt_m4a1
- cczmp_prop_vw_t6_black — g_spawn cczmp_prop_vw_t6_black

## What hasn't been done yet
The remaining 200 models are not converted. Both models are static objects; VW has no transport physics, the side door is closed and not animated. The source confirms the T6, but not specifically the T6.1 facelift.
The gaming test is not completed: the Windows session on the PC is blocked. Spawn and display in Anomaly has not been confirmed. No input was made to a locked session. User saves have not changed.

## Artifacts and backups
- VW preview: tools\vehicles_work\donor_pilot_vw_t6\vw_t6_ogf_preview.png
- VW test: tools\vehicles_work\donor_pilot_vw_t6\run_vw_t6_game_test_wait.ps1 (syntax checked; spawn: g_spawn cczmp_prop_vw_t6_black)
- General handoff: tools\vehicles_work\HANDOFF_RU.md
- VW pre: _backups\vw_t6_pre_20261013_110120
- VW post: _backups\vw_t6_post_20261013_110532, 60 files with SHA-256 in manifest.json
- M4 pre: _backups\donor_pilot_pre_20261013_063623
- M4 post: _backups\donor_pilot_post_20261013_104741


# Mass donor integration (updated 10/13/2026)

## Result
- All 202 archives from `tools\доноры` have been processed: 202 OGF, static physical props; Converting objects does not turn them into controllable vehicles, interactive weapons, or animated characters.
- DDS textures are installed for all models; The install manifest contains 202 models and 2041 DDS. Reconciliation of paths and sizes: there are no gaps or discrepancies in sizes.
- 202 sections `cczmp_donor_NNN` have been added to `gamedata\configs\cczmp\deadcity_objects.ltx`, each inheriting `cczmp_dc_prop`. `CREDITS_DONORS.md` updated.
- Sony Betamax (archive No. 67) at first did not pass the OGF limit on vertices; re-export with 50,000 triangles completed successfully.
- Fixed batch run summary: validator confirms 202/202 file sets, all licenses are stored next to staging.

## Backups and manifest
- Before installation: `_backups\donors_bulk_pre_20261013_173145` (154 files).
- After installation: `_backups\donors_bulk_post_20261013_173417` (2398 files, SHA-256 manifest).
- SHA-256 of the post-backup manifest: `D351A21016DFD734EB6CBC5205093E6D4B4EAE806DE4E7AD64F06C1C1C159FDA`.
- Detailed list of new OGF/DDS and SHA-256: `tools\vehicles_work\donor_bulk_install_manifest.json`.

## Check
File verification confirms the presence of all 202 OGFs, the matching sizes of all OGFs and DDSs, 202 spawner sections and the presence of the base class `cczmp_dc_prop`. In-game spawn and appearance in Anomaly have not yet been confirmed: the lock screen is active on Windows (`LockApp.exe`), Anomaly is not currently running.

# Checking interaction and spawn menu (10/14/2026)

## Changes
- A “Donor Models” section with categories of vehicles, weapons, NPC, equipment and other objects has been added to the F7 CCZMP debugging menu item. Within a category, models are grouped by source folders.
- A catalog of 202 models has been prepared: 39 transport models, 7 weapon models, 5 NPC models, 2 equipment items and 149 other objects.
- NPC groups are associated with organization folders: STO - Kaban, MChS, OMON, Ministry of Health, Alpha/Vympel.
- At F, donor objects open a card with name, type and category. Spawn places a physical layout on the nearest navmesh point in front of the player.

## Limits and verification
- Imported models remain static OGF layouts: vehicles are not controlled, weapons do not fire, NPC do not come to life and do not receive AI.
- Catalog, compliance of all 202 sections deadcity_objects.ltx and XML localization RU/EN was checked by the check_donor_catalog.py script.
- Lua 5.1 compile test for cczmp*.script passed. Of the 205 tests in the total set, 184 passed; 21 failed in the old UI/dialog test stubs (cczmp_runtime / cczmp_life_ui missing).
- Anomaly was launched for testing, but in a blocked Windows session the game window was stuck at “Not responding.” F7, F interaction and spawn in a live game could not be confirmed; no input was made into a blocked session.

## Backup before these edits
- _backups\donor_interaction_pre_20261014_063125 (102 files; SHA-256 manifest created before UI/interaction).
- In a separate Lua 5.1 mock test, we read the directory, issued groups, checked DEV_DEBUG and created a mock at the found navmesh point.
- After implementation, a post backup was created: _backups\donor_interaction_post_20261014_063935 (11 files, SHA-256 in manifest.json).
