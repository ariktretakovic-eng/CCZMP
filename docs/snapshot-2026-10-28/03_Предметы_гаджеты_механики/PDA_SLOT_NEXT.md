# Latest baseline: PDA contacts hotfix, 2026-10-10

Installed after the tuning release: gamedata/scripts/ui_pda_contacts_tab.script. Resolve online NPCs and story contacts with level.object_by_id rather than cached db.storage wrappers; enforce the 50-cell grid capacity. No changes to PDA models/HUD, engine executables or save format. Tests: tools/tests/test_cczmp_pda_contacts.py.

Original user crash: 12:48:19 dump, native clsid read at 0x1401b0766 with null native object. Baseline PDA 1/2/3 slot/UI/3D tests passed. Controlled stale-cache contact reproduction crashed in clsid's object-resolution path (0x1400df426), so do not claim the diagnostic test reproduced the exact original session history. Fixed version survives stale cache.

All 243 prior automated checks plus 11 new full Reset tests passed. Native fixed first + cold checks passed PDA 1/2/3 via inventory UI, slot, 3D, contact handler and rucksack with the same original instance IDs after cold load. Fixed first also checked stale wrapper skip. Logs in this directory.

Backup: D:\CCZMP PROJECT\_backups\pda_slot_20261010_131715 (new loose script; rollback removes only it). Cleanup: 40 original save files unchanged, user.ltx restored exactly, six private fixture save files and zz_cczmp_pda_slot_check.script removed; no owned Anomaly process left.

Release: D:\CCZMP PROJECT\releases\CCZMP_PDA_slot_fix.zip, 11,323 bytes, SHA256 6454533beabbf9aea9baab47916f9aec302dd7e76da5a211e5a8d439a19bcf09. Apply AFTER the previous full items/tuning archive. Local full source includes this override. Persistent artifact identity: libfile_4968e67a65f4819199a5cf79098ada74; receipt items_work/pda_slot/library_receipt.json. Prior full archive remains the base and does not include this overlay.

Feature development remains paused pending the user's new specification; bug fixes are separately authorized.
