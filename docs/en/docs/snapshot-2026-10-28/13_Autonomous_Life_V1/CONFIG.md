[Русский](../../../../snapshot-2026-10-28/13_Autonomous_Life_V1/CONFIG.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Autonomous Life V1 configuration

File: `D:\CCZMP PROJECT\gamedata\configs\cczmp\life_v1.ltx`.

The parameters are read when the game is started again. Default: up to 30 registered existing citizens, up to 12 events per update, target budget 1.5 ms, queue up to 4096 events. Search for existing residents - once every 5 seconds; This is a separate cost from the queue. A heavy single action may exceed the budget; need an actual profile.

`seed=28102026`: Applies only when creating a state; changing the seed does not reset the old world. The PRNG state is preserved.

`enabled=false`: the module stops advancing time and performing operations; the original life of three employees IC continues to work. The saved data remains. Resuming does not accrue income during the intentional stop of the simulator. To temporarily stop from the debug console: `cczmp_life_core.pause(true)`; renewal: `cczmp_life_core.pause(false)`.

`memory_limit=20`, `knowledge_limit=24`, `relationship_limit=12`: restriction of citizen data. Additionally, the latest 160 general events and up to 32 quarantine errors are saved. Quarantine overflow stops the simulator. Unique financial receipts are not deleted: limit 8192; when reached, new payments are rejected rather than old payments being forgotten.

`work_hours=8`, `state_wage=160`, `private_wage=80`: initial conditions of created contracts. An existing contract does not change size when editing the config. State salaries spend real treasury IC; with a zero treasury, an unpaid obligation remains. The private salary depletes the employer's account. The module does not create new budgets.

`meal_price=40`, `meal_nutrition=65`: consumption of a real food item, your own or from an existing seller's stock. Price - V1 setting, not the store's standard retail price. There is only one seller, interlocation delivery is not modeled. Lack of stock/money leaves the need unsatisfied.

`hour_hunger=4`, `hour_fatigue=4`, `rest_recovery=16`: indicators 0–100. Lack of food affects the utility of targets and the safety score. Physical offline damage to health has not yet been implemented.

`min_goal_hours=2`, `job_cooldown_days=3`: protection against frequent changes of goals/work. Position rules are described in `cczmp_life_careers.script`; Minimum shifts worked and vacancy conditions apply to all applicants. Changing the native community and issuing departmental authorities is not performed through a workaround.

Diagnostics: F6 → employee life → diagnostics. The number of citizens, offline, queue, game time lag, p95 queue time, errors, goals and reasons are displayed. `cczmp_life_core.diagnostics()` returns the same data for tools.
