# CCZMP baseline — 2026-10-10

Latest user request: pause feature development while the user prepares a new specification; explain in-game use and implementation; suggest a development-team name.

Installed project: D:\CCZMP PROJECT. Last completed stage: civilian suspension on purchased/debug Niva, UAZ-469 and W140 (wheel friction x1.15, 15,000 RUB). No Stage 1/2, lowered body, government tuning or aircraft implementation.

Release: releases\cczmp_items_tuning_20261010.zip; 8,060,717 bytes; SHA256 24ad60effe7e1c729db9ef8501d9964ef30a33b731be030ac5a9a1ab3c0e7804. 164 entries, 96 game files; manifest/CRC checked. Standalone guide text equals archive guide after CRLF normalization.

Backup: _backups\items_tuning_20261010_065503. Cleanup verified: all 39 original save files unchanged; user settings restored; six private fixture save files and temporary zz_cczmp_tuning_check.script removed.

QA: 243 automated tests (128 core + 51 items + 21 continuation + 21 locks + 22 tuning), 9 native asset checks. Actual Anomaly first and cold runs passed all three cars with original server ID/name/contract UID, 17L fuel and 61% health. Cold physics settling changed body tilt <1 degree. Intermediate spawn-placement and strict-angle failures are retained in logs. Native save/load during a pending tuning transaction and long road comparison were not separately checked.

Local deliverables: items_work/deliverables/CCZMP_items_hacking_engineering.zip and CCZMP_items_hacking_guide.md. Both persisted as version 2 under existing identities; successful receipt items_work/library_upload_tuning_result.json. Latest local gamedata: items_work/continuation/project/gamedata. Proof: items_work/tuning/verification.

Before implementing future specification: compare requested behavior against current guide and actual modules, preserve old save state and item identities, keep modal cleanup/F6/F7/inventory regression checks, stage independent changes and retain rollback manifest. Do not claim the original PDFs are fully implemented. New visual assets, buildings, voice/audio, drone flight and further transport remain unfinished.


Latest follow-up baseline: PDA contacts hotfix installed 2026-10-10. See D:\CCZMP PROJECT\tools\pda_slot_work_20261010\PDA_SLOT_NEXT.md. Apply releases\CCZMP_PDA_slot_fix.zip after the full tuning archive. 243 prior + 11 new tests, native first/cold PDA 1/2/3 passed; cleanup verified.
