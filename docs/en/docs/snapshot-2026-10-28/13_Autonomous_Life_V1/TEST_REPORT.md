[Русский](../../../../snapshot-2026-10-28/13_Autonomous_Life_V1/TEST_REPORT.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Autonomous Life V1 - inspection report, 10/28/2026

**Status: The minimum kernel from section 14 technical specification has been verified. Full V1 is NOT accepted. The usual warm loading went away after the correction; extended scenario after level change is not accepted.**

Environment: AnomalyDX9AVX.exe, real `D:\CCZMP PROJECT`, separate profile `tools/autonomous_life_v1/native_appdata`. Game seed: 28102026. The original test slot `_cczmp_ui_seed` was copied from the previous test profile. Custom appdata was not used for writing. Linked to 22 existing residents: 12 officers/patrol and 10 district residents, without creating duplicate populations.

## Native vertical

1. `native_setup.lua`: registers real residents and migrates three profiles IC; creates **test world only** 400 real bread items in the inventory of an existing merchant. Real accounts are not replenished.
2. `native_to_cordon.lua`: standard JumpToLevel for Cordon. No villager is transferred after the player.
3. `native_ten_days.lua` / `native_verify_ten.lua`: 10 game days and a gradual analysis of events. Resident p237, real object 15911: earned 960, spent 480, completed assistant → courier → coordinator. The original accounts of the employer and employee were changed by actual transactions.
4. `_cczmp_life_ten_days`: saving with a stopped queue. Complete completion of the process and a new start. `native_restore.lua` confirmed the equality of accounts, treasury, queue, profession, earnings and expenses; repeating the bank receipt does not change the balance.
5. Corrected version: `native_clock_regression.lua` - the jump of 86400 seconds immediately before the pause is taken into account; `native_final_ten.lua` / `native_final_ten_verify.lua` - another 10 days at Cordon. Another 400 real test items have been added for this test. **1800 earnings, 680 expenses, 17 meals; the total amount of accounts and treasury is 53352, stored accurately.** All 22 citizens OFFLINE; queue backlog 0; errors/quarantine 0.
6. `native_return.lua`: return to Dead City, previous object_id=15911, same UID, one NPC record, profession coordinator. All 22 are ONLINE again. The check waits for the actual readiness of client objects, rather than considering the first frame loading ready.
7. `native_social.lua` / `native_social_verify.lua`: dummy knowledge without real bunker transferred from p223 to p230 with a delay of 60 game seconds; The remaining 20 residents did not receive it globally.
8. `native_death.lua` / `native_death_verify.lua`: in **a copy of the test world** the current leader of the garage group p243 was killed; real death processed, successor p242, repeated hour did not resurrect the deceased.
9. Services: real call 111 through the phone without debiting money; ambulance 30012 with driver 30013 and three doctors was actually created. Existing taxi No. 1 ordered, canceled free of charge. The full ride and treatment in this passage have not been tested.
10. The native diagnostic screen opened and closed; control returned. Snapshot: `tools/autonomous_life_v1/life_ui.png` (reserved `current.png`).

The first check of the time jump revealed a loss of interval when the loading flag was set during a pause. Fixed by splitting loading and pause. The first item of food was identified as being blocked by an unpaid reserve; the choice now skips someone else's reservation, unsuccessful payment releases it. Separately, the lack of departmental ranks for civilians and the ability of employers to fill their own vacancies have been corrected. The original failed checks are saved in the log.

## Matrix LIFE-001…018

| Test | Status | Checked and remaining |
|---|---|---|
| LIFE-001 | PASS native | 22 existing NPCs outside of player level, work, real salary/food, change of plan. Repeated 10-day run after corrections. |
| LIFE-002 | PARTIAL | Utility takes into account hunger/fatigue, food is actually consumed; a separate native competition scenario for political purposes has not been implemented. |
| LIFE-003 | PASS native, narrow chain | Assistant → courier → coordinator through vacancies and experience. Political positions are not accepted. |
| LIFE-004 | PARTIAL | Actual death of leader and succession, links to members' accounts. Autonomous criminal earnings, hiring and transactions are not accepted. |
| LIFE-005 | PASS native | Test knowledge is not disclosed to citizens without a source; no real bunker is created. |
| LIFE-006 | PASS native | Delivery of information through a queue with a source and a delay. |
| LIFE-007 | MOCK ONLY | The witness's decision depends on the relationship/risk. The policy is not yet included in the actual consequence of IC. |
| LIFE-008 | PASS native | Exit to Cordon, cold loading, return with the same UID/ID without a duplicate. |
| LIFE-009 | PASS native, narrow profile | Coldly restored real accounts, queue, profession and expenses. Not a guarantee of all transport preservations. |
| LIFE-010 | PARTIAL native | First revision: 0xC0000005. After precache protection, the usual warm-load went through twice, saving accounts, queue, knowledge and death. Extended transition/repeat loading not accepted; old glitch 22.10 is not closed. |
| LIFE-011 | PARTIAL | Real online death and ban on new actions have been verified. Special native death outside the active level is not reproduced. |
| LIFE-012 | PARTIAL native | Call 111, car/crew, order and cancel a taxi. The full flight and medical cycle were not run. |
| LIFE-013 | PARTIAL | Native queue stopping, mock pause, rollback hash check. Full rollback is not accepted on a new clean installation. |
| LIFE-014 | PARTIAL | Real queue budget and LuaJIT 100/1000/5000; a full-fledged identical before/after rendering scene is not completed. |
| LIFE-015 | PASS native + mock | The receipt does not repeat the actual transfer; mock event repetition and protection against changing key parameters. |
| LIFE-016 | PARTIAL | Vacancy and successor of one real group. The vacancy of the head of state and departmental appointments have not been accepted in their entirety. |
| LIFE-017 | PARTIAL | Real return of the same NPC; There is no new NPC spawn/teleport in the code. The border physical route has not been tested separately. |
| LIFE-018 | PASS native, limited period | Jumps of 1 and 10 days, gradual catch-up, unique information event, zero final backlog. Missing years are not tested. |

## Logs and playback

Root of evidence: `D:\CCZMP PROJECT\tools\autonomous_life_v1`.

* `native_live.log` - sequence of commands and PASS/errors; `native_appdata/logs/xray_user.log` - engine.
* `native_initial.json`, `native_ten_days.json`, `native_cold_restore.json`, `native_final_ten.json`, `native_return.json`, `native_information.json`, `native_clock_regression.json`, `native_services.json`, `native_service_dispatch.json`, `native_death.json`, `native_ui.json`.
* Test slots: `_cczmp_life_initial`, `_cczmp_life_ten_days`, `_cczmp_life_final` in a separate native_appdata.
* Launch: `python "D:\CCZMP PROJECT\tools\autonomous_life_v1\native_runner.py" _cczmp_life_ten_days`. A strictly limited profile `native_probe.script` is temporarily installed in the test assembly under the name `zzzz_cczmp_life_owned.script`; it is removed from the final gamedata.
* Commands are sent `send.py <native_*.lua>`, sequentially after the end of the previous one. `--END` is a marker for a completed file. The loading screen requires input into the window belonging to the test; native input_owned.py checks PID before input.
* LuaJIT mock: `python ...\test.py` - **21 PASS**, `mock_results.json`. `python ...\bench.py` - `mock_benchmark.json`. These are not native X-Ray tests.

Early fixture errors - checking materialization too early and attempting to serialize a diagnostic native value - are not counted as successful tests. They are not hidden from the log. On successful offline runs, there were 0 errors for the new handler and quarantine events.

## Failure loading

Current dump: `crash_evidence/xray_user_10-28-26_23-15-47.mdmp`, address `0x14014A46C`, reading address `0x8` at `r9=0`. Instructions: `mov rax, [r9+8]`.

Old dump 10/22: `0x14014A497`, reading `0xA`. Both addresses refer to the same machine function starting `0x14014A450`, but different instructions. This comparison **does not establish a definitive cause** and does not in itself prove the absence of regression. The control run with the source runtime files is described separately in `WARM_LOAD.md`. The entire save/load cannot be considered accepted based on one successful cold-case.

## Failed conditions of full V1

Clean new game, full old user save, full warm-load matrix, social policy in IC, change of organization, autonomous criminal income/hiring/deals, expanded online scheduler, full set of professions and controlled FPS comparison remain open. Historical PASSes do not replace them.

After the initial crash: control with the original runtime scripts without a kernel passed. The native kernel has removed access to the clock during precache/initial pause. Two normal warm-loads passed after that, confirmed by `native_warm_first.json` and the subsequent log. Knowledge, long-term goal and death are tested separately. The test render-clock is not included in the release. An additional check for changing cards first stopped on a deferred game timer, then an immediate call to the regular test ChangeLevel completed the process (dump 00:07:42). Such a run is not counted and is not issued as a confirmed engine fix.

## Final regression of the initial profile

Fixed a bug in the old life adapter: the kernel-managed profile first has phase initialized before the old callback forms its state. A 21st mock test has been added, executing the actual old module and its actor callback. Native repeat `_cczmp_ui_seed` passed: `native_auto_bank.json`, AUTO_BANK_NATIVE_PASS. Production bridge, after state_mgr was ready and crime-init was completed, 22 existing accounts were opened for 22 citizens. Without manual account_state in the test and without issuing money: merchant 5400 bank + 3600 cash = original 9000; bank 900 employee. The main actor callback has been verified. Errors/quarantine/backlog 0. This is a check for the start of an existing test slot, not a clean new game.
