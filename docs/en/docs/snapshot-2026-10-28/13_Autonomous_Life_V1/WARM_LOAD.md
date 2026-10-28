[Русский](../../../../snapshot-2026-10-28/13_Autonomous_Life_V1/WARM_LOAD.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Separate check warm loading

The initial new run of `_cczmp_life_final` ended in a crash, so the overall acceptance testing V1 has not been announced. This is not a missed test.

| Run | Result | Terms |
|---|---|---|
| New kernel, first revision | FAIL | After Cordon and return to Dead City, save/load in one process. 0xC0000005 to 0x14014A46C, read 0x8, r9=0. |
| Original runtime scripts without the new kernel | PASS, one control | The same saving `_cczmp_life_final`: cold-load → warm-load → actual entry into the world. `rawget(_G,'cczmp_life_core')==nil`. |
| Corrected protection loading | PASS, two regular reps | Checked accounts, queue, profession, knowledge, long-term goal and death. The active option function contains a new cache upvalue. |
| Additional level changes | NOT ACCEPTED | The delayed transition in test mode stopped on the timer; immediate test-API terminated the process, dump 00:07:42. This result is not used as evidence of stability. |

For control purposes, three original scripts were temporarily restored and six new modules/configs were removed from runtime; their current bytes are stored in `tools/autonomous_life_v1/control_current`. After control, the entire installed patch was restored, third-party files and user saves were not changed. The control slot itself was not overwritten.

Reason for correction: Legacy `update` called `clock()` during precache on `loading=true`. In such a state, one cannot rely on the readiness of the actor and his pstor. Now precache and initial pause return control before any time manipulation; the usual pause after loading continues to preserve the correctness of the game time jump. With `enabled=false` update, death and load do not create life operations.

This is a specific fix to its own lifecycle. **The exact cause of the C++ access violation has not yet been determined**, and the ownership of the address of the old function is not evidence that the original transport defect has been corrected.

Dump comparison:

* 28.10: `0x14014A46C`, `mov rax,[r9+8]`, r9=0.
* 22.10: `0x14014A497`, reading 0xA.
* Both addresses are in the machine function from `0x14014A450`. C++ symbol names are not confirmed.

Artifacts: `crash_comparison.json`, `crash_evidence/warm_crash.log`, minidump, `control_warm_result.json`, `native_live.log`. The original logs were not cleared. You cannot pass off a part-stack match as a proven common cause.

Fixture uses render-clock strictly tied to its own profile to remove the boot pause and read commands; it has been removed from the final gamedata. An early filter on an unchanged time_global prevented the following commands from being read in a stopped test time; fixed only in fixture. These changes are not features of the simulator. Details of unsuccessful runs are left in native_live.log and final_driver_result.json.
