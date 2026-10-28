[Русский](../../../../snapshot-2026-10-28/13_Autonomous_Life_V1/REPORT_RU.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Autonomous life CCZMP - embedded V1 kernel

**October 28, 2026. Status: Minimal vertical implemented and tested in Anomaly; complete V1 for technical specification NOT completed and NOT accepted.**

`D:\CCZMP PROJECT` has an event simulator installed for the 22 existing residents of Dead City. It stores UID and ALife, needs, goals, memory, limited connections, knowledge and queue. NPCs outside the player's location work, spend real money/food, and change professions through vacancies. There is no second bank balance or population respawn.

In a repeated native run of 10 days at Cordon, the employee received 1800 from the employer’s account, spent 680 on 17 meals; the total amount of money remained the same. The chain assistant → courier → coordinator and cold loading was previously checked without re-payment. Returning to Dead City restored the same 22 residents online with the same IDs. Verified address information, death of group leader/successor, 111 with real ambulance and crew, taxi order/cancellation, native diagnostics.

**acceptance testing limitation: the first warm loading caused 0xC0000005.** After precache protection, two regular warm-loads passed with data saved; additional transition script is not accepted after process completion on immediate test-API. The dumps and test run are saved. The fix for the old transport crash 22.10 and the general stability of saves are not announced. Details - `WARM_LOAD.md`.

Six new modules have been implemented, a separate config; The bank, old life and its diagnostics have been minimally changed. The general actor/bind_stalker/xr_logic has not been rewritten. Backup of 140 files and hashes available in tools/autonomous_life_v1; The initial 47 user save/settings files are checked separately. Changed files and SHA256 - `FILES.md`, short patches - `PATCH.diff`.

Physical food has a finite source. Two test stocks of 400 items are created exclusively in a separate test profile; The release code does not show these reserves. The treasury is not replenished automatically: unpaid wages remain a liability.

Groups retain real members and continuity, but autonomous heists, recruitment, and deals are not yet implemented. The witness policy is not involved in the investigation. The native schemes of all NPCs have not been replaced by a full-fledged GOAP; close behavior of three employees IC saved via adapter. See `KNOWN_LIMITATIONS.md`.

Documentation:

* `API_CONTRACTS.md` - real APIs and architectural connections.
* `integration_map.md` - integration map compiled before the changes.
* `CONFIG.md` - limits and shutdown.
* `TEST_REPORT.md` - LIFE-001...018 with honest native/mock statuses.
* `PERFORMANCE.md` - individual metrics and interpretation limits.
* `ROLLBACK.md` - disable/rollback and check subsequent changes.
* `WARM_LOAD.md` - crash and control run.

Historical documentation has been preserved. The indexes are supplemented with links to this stage. This is the basis for the next stage, and not the announcement of the entire autonomous life of NChG ready.

Final check of the original test slot after adapter correction: 22 citizens / 22 real bank accounts, no test funding. The merchant has 5400 in his account + 3600 in cash = original 9000. The temporary test module has been removed from gamedata.
