[Русский](../../../../snapshot-2026-10-28/13_Autonomous_Life_V1/PERFORMANCE.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Performance and saving

**Full before/after comparison of the same scene is not accepted. The numbers below describe individual runs and do not prove the absence of FPS regression.**

Native queue, repeated 10-day catch-up of 22 real OFFLINE citizens, until the latest optimization of reading the config:

| Indicator | Result |
|---|---:|
| Processed events in progress | 6639 |
| Measurement Window Size | 2048 update |
| Average queue time | 0.909 ms |
| p50/p95/p99 | 0 / 2 / 3 ms |
| Final backlog | 0 game seconds |
| Final queue | 106 events |
| Bugs/quarantine | 0 / 0 |

Future hours and repeated demands for unpaid treasury wages remain in the queue; a non-zero queue does not mean backlog. `pump` is measured, not the entire search for residents/AI/render. The `os.clock()` indicator has approximately millisecond resolution: zero does not mean free execution. 1.5ms budget checked between events; a single native action is not interrupted. The target budget of 1–2 ms is not met for all p99 in this catch-up.

After this, reading immutable LTX parameters is cached to the process. A full repeat of the native 10-day profile was not performed on this latest optimization; functional equivalence was verified by 21 mock tests. You cannot pass off old numbers as a new profile.

LuaJIT 5.1, logical citizens with mock adapter; one hour of events, no X-Ray or graphics, final code:

| Logical NPCs | Total processing | Average update | p95/p99 update | Final backlog |
|---:|---:|---:|---:|---:|
| 100 | 3.61ms | 0.444 ms | 1 / 1 ms | 0 |
| 1000 | 17.75ms | 0.190 ms | 1 / 1 ms | 0 |
| 5000 | 86.06 ms | 0.191 ms | 1 / 1 ms | 0 |

Creating a fixture is not included in these numbers. The release limit is 30 citizens. These tests did not create 5000 physical NPCs or measure the game's FPS.

Native source profile without new kernel: 495 frames Dead City, average 52.45 ms, p95 74 ms, p99 180 ms. The camera position and dynamic world states differed in later tests; comparison with them is not controlled before/after. A full run in the same scene remains mandatory for V1 acceptance.

Native custom-save files:

* `_cczmp_life_ten_days.scoc`: 1,505,989 bytes;
* `_cczmp_life_final.scoc`: 1,684,173 bytes.

This is **all custom-save**, including the previous subsystems, test receipts, bread and detailed proof; the difference cannot be attributed to the simulator alone. Cold loading passed first. The first attempt to warm-load the second one ended in crash; after protection loading, regular retries have passed, the extended route has not been accepted; see WARM_LOAD.md. Stand-alone partition: 157,942 bytes; 20 native marshal round-trip. Encode: average 1.75 ms, p95/p99 2/2 ms. Decode: average 1.70 ms, p95/p99 2/3 ms. This is a CPU encode/decode table, not a full save I/O. The entire Lua heap at the measurement point is about 56,080 KiB; The share of the simulator alone is not measured separately. Late render profile Dead City: 2274 frames, average 25.84 ms, p95/p99 32/51 ms; different camera/weather/state of the world, so FPS improvement is not proven by this.

Sources: `native_final_ten.json`, `mock_benchmark.json`, `baseline_native.json`, files in native_appdata/savedgames. All are in `tools/autonomous_life_v1`.
