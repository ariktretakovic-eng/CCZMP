[Русский](../../../snapshot-2026-10-28/CCZMP_AUTONOMOUS_LIFE_V1_TECH_SPEC_RU_2026-10-28.md) · **English** · [Documentation index](../INDEX.md) · [Translation notes](../../TRANSLATION.md)

# CCZMP Autonomous Life V1 - technical specifications for the autonomous life of NPCs

**Project:** STALKER X CCZMP · S.T.A.L.K.E.R. Anomaly 1.5.1 / X-Ray  
**Document version:** 1.0 · 10/28/2026  
**Address:** AI developer working with real catalog `D:\CCZMP PROJECT`  
**Status:** technical specification for implementation; this file **does not** mean that changes have already been made to the game.  
**Basic source:** `CCZMP_PROJECT_FULL_REPORT_2026-10-28.md` (project audit dated 10/28/2026).  
**Priority:** maintain compatibility of working mechanics and saves; first working vertical V1, then expansion.

---

## 0. The task for the execution AI is to read first

Create **the first real version of the global autonomous life of the population NChG**, in which NPCs retain personality, memory, connections, money, goals and change occupations/social status **regardless of whether the player is in their location**. NPCs outside the active location should continue to live in a **simplified event simulation**, and when entering online, consistently materialize in the existing X-Ray/A-Life systems. Don't turn all plot outcomes into `if/elseif` for individual characters.

**V1 is considered completed only after integration into the existing project files, native in-game checks and a report with paths, logs and reproducible scripts.** You cannot claim a demo Lua file or a separately launched Python simulator for implementation in Anomaly.

**Inviolable:** active NPCs, their ID and ALife, passport system, 111, investigation IC, taxis, patrols, transport, orders and money. It is prohibited to erase saves/replace identifiers/rewrite entire modules without analyzing dependencies. Before modification - a backup copy of the modified files and a list of integration points.

**Essential criterion:** if a player is on the Cordon for 10 game days, a resident of Dead City must still receive a salary, spend resources, make personal decisions and, if there are reasons, change jobs; the criminal group must develop or degrade outside the presence of the player. Not every NPC is required to become President, but **everyone** should have general accessible career transition rules; the position of president should not be strictly blocked by the original profession (subject to the established legal conditions).

---

## 1. Actual starting point (by audit, not by assumption)

1. Current database: Anomaly 1.5.1 / X-Ray, `D:\CCZMP PROJECT`; 90 CCZMP scripts, active registry of 41 organizations. Numbers are a snapshot of the audit, **not a guarantee of absence of subsequent changes**.
2. `cczmp_life.script`: experimental life **of three employees IC** - schedules, needs, trust, memory retention (12 memories), simplified background calculation, separate confirmed cold loading. Requirements do not yet provide full food consumption/harm to health. **Do not rewrite blindly - expand via a compatible adapter.**
3. `cczmp_city_model.script` / `cczmp_city.script`: city events, reputation of a witness/district/organization, property relations/real deliveries. `cczmp_deadcity.script`: crime-ridden area (10 permanent residents, two companies and limited economic cycle). The report does not confirm a ready war OCG for the entire Zone.
4. `cczmp_investigations.script`, `cczmp_emergency.script`, `cczmp_response.script`: witnesses, investigations, 111 services, departure queues and real ALife NPCs. Do not replace them with global fictitious events.
5. `cczmp_bank.script`: personal accounts, transfers, loans and records; do not create a second independent character balance that conflicts with the bank. There is no complete corporate ledger yet.
6. `cczmp_transport.script`, `cczmp_taxi*` (check the actual names according to the project): car and taxi systems already exist; Do not create a second transport-owning component.
7. Physical transport of service crews uses binding to real ALife NPCs and CCar restrictions; Existing boarding, calling and returning patterns are required to be respected.
8. There is a recorded **unexplained warm-load crash `0xC0000005`** in one of the transport test profiles on 10/22. Cold recovery of two specific cars is successful, but this does not prove the overall correctness of the saves. The introduction of V1 should not mask or aggravate this defect.
9. It **does not follow** from the report that the online server has already been implemented. V1 is offline, with data boundaries convenient for future server-side authority.

**Required Action:** Before writing code, find these files, read the actual exports/hooks/save structures, and describe a compatible contract. The names listed are search guidelines and not confirmation of the existence of the specified functions/APIs.

---

## 2. Strong design principles

- **Independence from the player.** There is no condition like `if level.name()==... then npc_life()` as the only source of life decisions. Simulation of time/events is carried out for the whole world.
- **One personality - one source of truth.** `citizen_uid` is stable and not equal to the temporary object id; ALife object id may disappear/reused. The mapping is updated and validated.
- **Same rules for player and NPC, different controllers.** Rights to profession/position/money/property are determined by the domain system. Controls in V1: NPC = AI, GG = human; Do not sell online.
- **Awareness is limited.** NPC/OCG knows only the information available to them: personal experience, publicly available news, messages from trusted contacts, the results of their own actions. No global telepathy about a secret bunker.
- **Causality and verifiability.** Changes must be generated by specific available actions/events; with a record of causes, authors, times and results.
- **Easy background life, detailed close-up life.** No one is “frozen” outside of online; Only the accuracy of physics/navigation/step-by-step activity changes.
- **Transactional.** You cannot pay a salary twice, issue an item twice, or “resurrect” a killed NPC due to loading/level change.
- **Determinism for tests.** Seed PRNG, stable order of events at equal times, event identifiers, result tracing.
- **Performance on budget.** Don't run the full scheduler on every NPC every frame. Any hard work is limited and/or event-driven.
- **Do not replace the simulation with a text generator.** LLM, Internet, KoboldCPP and external APIs are optional for V1. Work offline.

---

## 3. Boundary V1: what is obligatory, what is deferred

### 3.1 Required functionality V1

1. Register of citizens with identity, profession, organization, position, current/home location, state of life, characteristics, goals and limited memory log.
2. Needs (hunger, fatigue, security, income/liabilities), time and limited personal spending patterns. First integrate real money/items; Mark inaccessible vital services with an explicit abstract operation with a record; do not create a resource “out of thin air” without rules.
3. Event queue in **game time** with separate periodic “hourly/daily” processes and deduplication.
4. Utility scoring of available goals and a limited GOAP/task scheduler or an ordered library of preconditions/effects, without endless brute force.
5. Available actions: work/get paid under an existing contract, rest, buy or consume basic food (if there is a source), look for a job, apply/change profession (if there is a vacancy and conditions), communicate/transmit information, join/leave an organization according to rights, make a limited criminal decision, respond to death/arrest/debt.
6. Social relations: acquaintance, trust, loyalty, hostility, connection with the organization, delayed exchange of information; suppression of evidence by criminal witnesses as a configurable rule with exceptions based on identity/danger/relationship (not an absolute "all gangsters are always silent").
7. Life cycle of a criminal group: formation/hiring, income/expenses from real sources, leader status, influence and territory as **logical** V1 values, disagreements/breakup/deals. You cannot automatically give her heavy weapons, money and power.
8. Citizen’s career cycle: accessible transition “low-paid job → search for a vacancy → training/qualification (if implemented) → new job → participation in the management of the organization.” Political career through **expandable rules**, not forced change of president on a timer. For V1, implement at least one verifiable promotion chain and vacancy/appointment mechanism. Full elections are NOT required.
9. Internal OFFLINE/ONLINE status with serialization and soft transfer of plans to standard AI schemes; do not carry out remote simulated combat with physical projectiles.
10. HUD/debug F6/F7 or separate secure diagnostic interface/log: NPC status, current target, upcoming event, reason for target change, current number of events and update duration.
11. Saving/cold loading: without re-accrual and without loss of long-term goals/connections, including changes in location and death of NPCs.
12. Configuration of activation and restrictions of the simulation without violating the current profile/save; migration of existing three NPCs IC.

### 3.2 Explicitly NOT required in V1

- Physical simulation of each resident on all maps at the same time; 100+ completed professions; families, births and divorces; full government and elections; corporate economics/industry; multi-user synchronization; Full Speech/Local LLM; real navigation of each remote taxi driver; autonomous tactics of full-fledged war OCG; believable physics of the Gustav and all new cars.
- Working C++ multi-threaded integration or separate process **optional**. First measure the cost of events in Lua, and only with a proven limitation justify a native backend.

---

## 4. Suggested modules (names adapted to real naming)

| Module | Responsibility | Important Limitation |
|---|---|---|
| `cczmp_life_core.script` | Vital status API, citizen registration | Do not duplicate identity/passport |
| `cczmp_life_events.script` | Min-heap queues, deduplication, game time | Don't do an infinite catch-up in one frame |
| `cczmp_life_goals.script` | Utility scoring, rules for selecting targets | Only known NPC facts |
| `cczmp_life_plans.script` | Preconditions/Effects, Constrained Scheduler | Search depth/cost limits |
| `cczmp_life_social.script` | Relationships, knowledge, dissemination of information | Do not reveal hidden data to the whole world |
| `cczmp_life_careers.script` | Jobs, vacancies, positions, promotion | Checking the rights of existing organizations |
| `cczmp_life_orgs.script` | Group goals, leaders, resources | Don't create a second faction system |
| `cczmp_life_bridge.script` | Linking X-Ray/A-Life and CCZMP systems | Only proven native APIs |
| `cczmp_life_persist.script` | Save/load scheme, migrations, versions | Idempotency + UID check |
| `cczmp_life_debug.script` | Logs, counters, testing tools | Disabled in release |

These are **target logical boundaries**, not an order to create exactly 10 separate Lua files. First set the loading script rules in a specific assembly and prevent cyclic `require`/initializations.

---

## 5. Data contracts (scheme example, adapt for Lua and existing serialization)

```text
Citizen {
  schema_version, citizen_uid, character_identity_ref, alife_id?,
  alive, current_level, logical_location_id, home_location_id,
  faction_id, organization_id?, role_id?, rank_id?, occupation_id?,
  employer_id?, wage_contract_id?, money_account_ref?, inventory_ref?,
  stats: { hunger, fatigue, safety, health, ambition, greed, loyalty, risk_tolerance },
  knowledge_ids[], relationship_ids[], memory_event_ids[],
  goals: { active_goal_id?, long_term_goal_ids[], plan_step?, decision_reason? },
  activity: { action_id?, state, started_game_ts?, ends_game_ts? },
  updated_game_ts, next_eval_game_ts, revision
}

WorldEvent {
  event_id, event_type, due_game_ts, priority, actor_uid?, target_uid?,
  source_event_id?, context_refs{}, expected_revision?, status,
  idempotency_key, created_game_ts, committed_game_ts?
}

Knowledge {
  knowledge_id, fact_type, subject_ref, source_uid?,
  confidence, acquired_game_ts, disclosed_to[], visibility_scope,
  expiry_game_ts?, is_verified
}

Relationship {
  uid_a, uid_b, trust, respect, fear, hostility, allegiance,
  last_interaction_game_ts, revision
}

OrganizationState {
  org_id, leadership_uid?, member_uids[], funds_ref?,
  resource_refs[], influence_by_zone{}, strategic_goal_ids[],
  learned_knowledge_ids[], revision
}
```

**Storage rules:** schematic versions; monotonous revision; fixed range of indicators (for example 0..100); links to real sources of funds; uniqueness of `event_id` and `idempotency_key`; compact memory lists (last N + important “anchor” events), not an endless text log inside the save. The field names are conditional; compare them with the structure of the current code.

### 5.1 Game Time Contract

- Use canonical CCZMP/X-Ray game time (find actual source and determine unit type).
- The queue is processing `due_game_ts <= now_game_ts`; with loading, completed transactions are applied first, then limited catch-up events.
- Time jump, sleep, map change and loading should give a consistent result; actions are not executed again due to re-entering update.
- For periodic income/expenses, store **the last paid period**, and not just the time of the next payment.
- Provide a limit on lag/long absences and aggregated recalculation for similar everyday events; Don't miss the unique implications of deaths, warrants, and ownership changes.

### 5.2 Integrity Contract

- An NPC should not have two mutually exclusive jobs/trips running at the same time.
- `alive=false` prohibits new labor, combat and conversational actions; allows for the consequences of death and the actions of other NPCs.
- Including an NPC in the global registry should not create its physical counterpart.
- Changes to property/money/items go through existing services and are verified after the transaction is completed.
- Notification of a crime is not equal to evidence of guilt; separate hearsay, testimony, established fact and procedural status.

---

## 6. Decision making: not spaghetti of if/else

### 6.1 Target selection

For NPCs, calculate the utility of **only currently achievable goals**; for example:

`score(goal) = base_weight + need_pressure + personality_fit + social_pressure + expected_benefit - risk_penalty - resource_cost - cooldown_penalty`.

Numerical coefficients are a configuration, not hard-wired “plot” names. A hungry janitor may choose food over career advancement; ambitious and wealthy - searching for a vacancy; frightened bandit - leaving a dangerous group.

**Anti-bounce:** hysteresis, minimum goal commitment window, cooldown for changing jobs/factions/strategies; emergency events (threat to life, arrest, death of a leader) can interrupt the normal plan.

### 6.2 Action Plan

Each action is registered as configuration/code with the same contract:

```text
ActionDefinition {
  id, prerequisites(state, knowledge), estimated_cost, estimated_duration,
  reserved_resources, world_effects, start(), tick_or_resolve(),
  on_cancel(), on_failure(), can_run_offline, can_run_online
}
```

**Actions for V1:** `work_shift`, `rest`, `consume_food`, `seek_job`, `apply_job`, `switch_job`, `learn_skill` (if there is a gaming infrastructure), `share_information`, `join_org`, `leave_org`, `recruit_member`, `negotiate`, `earn_criminal_income` (only if source available), `react_to_death`, `travel_abstract` (via verified route/time), `report_incident` (via existing service interface).

Do not implement the general "magic" `execute_action` that directly changes the real balance, permissions, owner or ALife without checking existing domain modules.

### 6.3 Scheduler limitations

- bounded search: maximum depth/nodes/milliseconds per solution, put default values in the config;
- postpone re-evaluation of the goal in the absence of new events;
- if it is impossible to perform an action - a known reason, cooldown and recalculation of the alternative;
- if there is insufficient budget, continue on the next beat, do not block the frame;
- deterministic order of alternatives with the same score.

---

## 7. Online / offline, A-Life and alignment with reality

**Offline:** count monetary transactions, personal decisions, changes in work and reputation, transfer of information, movement through the graph in an aggregated form; NPC state exists regardless of level load. Eliminate costly physics/animation/level navmesh pathfinding for deleted characters.

**Online:** existing X-Ray NPCs perform physical actions; the global simulation issues tasks to them through compatible circuits/adapters without overwriting the standard AI every frame.

**Entering the location:** check the UID/ALife id, restore the logical position at a valid point according to the game rules, compare the active plan with the visible scene, do not create a duplicate and do not teleport the observed objects. In the event of a conflict between the real world and the background plane, the main thing is considered to be a confirmed event in the game world with logging of the conflict.

**Exit location:** save inventory/money/position/case/transport status, continue the current task in the background, do not create a duplicate action (for example, a second taxi trip).

**Level Transitions:** For V1, existing game graph/A-Life routes and timing estimates can be used; if the route is unavailable, record the failure rather than instantly transfer the NPC. Confirm the real API on this build; inventing native methods is prohibited.

**Long-Range Events:** outside of observation, do not model animation, but change the world through verifiable consequences. You cannot declare a character killed by a random “combat simulation” if this conflicts with the active task/protection of a story NPC or the presence of a player nearby.

---

## 8. Rules of social relations, crime and public service

1. Attitudes towards witnesses are determined by personality, affiliation and context. The conditional “brothers” may refuse to testify against a common criminal, but loyalty, resentment, fear, conflicts OCG, coercion or a deal can change the decision. Aggression towards a government employee must go through the normal rules of detection, hostility and combat; no automatic shots “from the other end of the map.”
2. Organizations take on a life of their own: leadership, resources, goals, membership, credibility, and publicity. The disappearance/death of a leader triggers the event of choosing a successor or a split according to the rules.
3. Growth OCG requires a **real** source of income, access to people, infrastructure and expenses; you cannot “add +100 members” from one leader’s decision.
4. Discovering a secret facility (such as the underground complex containing the Gustav) in V1 is a **test case of universal knowledge**. Coordinates/information are transmitted only to participants who received the information; knowledge can be stored, sold, or communicated to the organization. The bunker itself, the equipment and its ownership should not appear without existing game resources and appropriate integration (in V1 a mock knowledge event is allowed for testing).
5. IC, MVD, OMON, ambulance, taxi and service crews continue to use the current modules. The social simulator generates requests/goals through their public interfaces and does not replace existing dispatching.
6. Offline, laws and sanctions are not introduced without existing procedural actions; job loss and wanted status are individual facts, not a universal “evil/good” field.
7. The death of a president or other leader should cause a **vacancy event and transition rule trigger**, and not an endless crash/empty link. Full election mechanism - future version; in V1, a correct “position vacant” state and a controlled assignment in the test system are sufficient.

---

## 9. Performance and scaling

### 9.1 Profiling first

Separately measure: simulator time per frame (p50/p95/p99), growth of the event queue, number of overdue events, serialization time, save size, memory, map change time, FPS/frametime before and after installation. Carry out in the same scene with the same configuration and seed; distinguish between rendering hardware limitations and AI load.

### 9.2 Budget processing

- Event-based min-heap/equivalent instead of completely enumerating NPCs every frame.
- Scheduled recalculation of Utility for inactive NPCs - sparse and spread over time; instant recalculation in case of significant events.
- Simulation budget **customizable**, initially targeting no more than 1-2ms per game frame in a typical run; This is a **target budget, not a promise**. Check lags in 30–40 FPS conditions.
- Mandatory events of high importance are served first; in case of a long lag, provide the metric `lag_game_seconds`.
- Reasonable limits on knowledge caches/connections/logs. Keep concise summaries of old episodes while retaining critical facts.
- When simulating 100/1000/5000/10000 logical NPCs, the load test does not have to mean a physical spawn of 10,000 NPCs; in the release, consider the maximum from the configuration and actual resources of the world.

### 9.3 If Lua is not enough

Possible stages are: C++ module or separate local service. Implement only after a reproducible profile. Any worker threads/external process work with an **immutable snapshot of data** and return a list of commands; only the main thread calls the X-Ray API, checks `revision` and applies events. No working with live CGameObject/ALife directly from a third-party thread without proven thread safety guarantees.

---

## 10. Development stages and concrete results

### Stage A - reconnaissance and protection of existing assets (mandatory)

- Remove the current list of scripts/configs/dependencies, hashes of affected files, create a backup; read working `cczmp_life.script` and save formats.
- Record public APIs of identity, money, organizations, rights, transport, events and A-Life; Find out the valid way to create/update citizens.
- Prepare a list of conflicting hooks and changes that will not be made.
- Save `docs/` original audit and separate `integration_map.md`.

**Result:** integration map + minimal patch plan, without touching other people's code before analyzing it.

### Stage B - minimum core of 10–30 citizens

- Registry UID, saving, event queue, Utility, vital needs/work/leisure, debug.
- Connect the existing three employees of IC and a small group of other current NPCs; no respawn.
- After 10 game days outside their level: at least one work/salary event, one expense/need, one change of plan; recovery after a cold save/load without duplicates.

**Result:** native reproducible vertical script.

### Stage C - careers, dating, criminal group

- Job vacancies/occupational transitions, relationships and knowledge sharing; growth/disintegration of at least one limited criminal group with a budget and people taken into account.
- Safe management succession event; potential government careers are modeled through general requirements/vacancies, not through scripted teleport to the presidency.
- “Bunker rumor” scenario: two NPCs find out at different times, the third remains unaware; The organization reacts only after receiving information.

**Result:** proven change in the structure of the world outside the player’s location.

### Stage D - Integration, Load, Regression

- Borders online/offline, save/load, transitions, death, dismissal, arrest, transport/taxi/111; eliminate data owner conflicts.
- Profiles of 100/1000/5000 logical citizens, check upper budget, queues and FPS degradation.
- Update module index, configs, disable/rollback instructions, current `installed` manifest.

**Result:** Stable installable V1 with test results and known limitations.

---

## 11. Acceptance scripts (mandatory automatic + native)

| ID | Script | Expected result |
|---|---|---|
| LIFE-001 | Registering an existing NPC | UID/passport/ALife is saved, no duplicate occurs |
| LIFE-002 | 10 game days player away | NPCs work/live/solve problems without visiting the level |
| LIFE-003 | Profession → vacancy → transition | If the conditions are met, the NPC actually changed employment, the records are consistent |
| LIFE-004 | Small OCG gained income/lost a leader | Money was not created out of thin air, continuity or schism is reproducible |
| LIFE-005 | Inaccessible knowledge about the bunker | NPC without a source of information does not know the coordinates |
| LIFE-006 | Transferring information to contact NPC | The recipient finds out at an acceptable moment, the source is fixed |
| LIFE-007 | Criminal witness and IC | The decision is a matter of loyalty/risk/relationship; witness may remain silent |
| LIFE-008 | Level change and re-entry | No second NPC/salary/inventory, plan continues |
| LIFE-009 | Cold loading | Finances, goals, relationships and queues recovered exactly once |
| LIFE-010 | Warm loading | No new crash; known crash from audit separately diagnosed |
| LIFE-011 | NPC died outside the current level | Does not return to work; consequences for other NPCs remain |
| LIFE-012 | The player called 111/got into a taxi | Existing mechanics work as before |
| LIFE-013 | Pause simulation/rollback mod | The main game remains functional; no save loss |
| LIFE-014 | Load 100/1000/5000 NPC | CPU/frametime/queue metrics are fixed, limits are formulated |
| LIFE-015 | Process one event_id twice | The result of a financial/legal transaction is applied only once |
| LIFE-016 | Vacancy of the head of the organization | There is no inactive leader_uid, departmental rights are not broken |
| LIFE-017 | Offline/online at the edge of traffic | No teleport in front of the player and double completion of the task |
| LIFE-018 | Time transition/sleep/lots of delay | The queue gradually catches up with time without freezing and losing unique events |

**For each test:** setup, input parameters, seed, time/location, exact steps, tested values ​​before/after, log, PASS/FAIL status and reason. A mock test does not replace a native test, and old PASSes do not replace checking a current build.

---

## 12. Quality, compatibility and rollback

- Patches are minimal. Connecting new code through existing extension points; if there is no API, add a narrow adapter and tests.
- No unreasonable changes to `actor`, `bind_stalker`, the general saved schema, `xr_logic` and other base files. If necessary, explicit diff, explanation and verification.
- Persistence with `schema_version`, migration of old profiles and fail-safe on a damaged individual record without erasing the entire world. **Do not use automatic save reset as a repair method.**
- Protect individual sources of truth: bank account, documents, property, warrant, physical transport and real NPC object.
- We need error logs with `citizen_uid`, `event_id`, `goal_id`, `game_ts`, duration and link to the module; do not record unnecessary secrets/personal data from external sources.
- Rollback is possible only with verification of modifications made after installation; do not roll the old package over the new assembly without checking the hashes.
- Requires a test on a new installation from scratch, a separate test save and an old save; Do not overwrite existing user work saves.
- Do not affect current licenses and assets; the release package should not include test `zzzz_cczmp_*_owned.script` without informed justification.

---

## 13. What the AI must convey upon completion

**Don’t answer with just “done.”** Send:

1. List of created and modified files with absolute paths; brief diffs/hashes, list of saved backups.
2. Architectural diagram of real connections and `API_CONTRACTS.md` with confirmed game functions (not fictitious).
3. `CONFIG.md` for limits, event budget, NPC count, debug, seed and the ability to disable the simulation.
4. `TEST_REPORT.md` with LIFE-001...018, logs, screenshots/reproducible commands if possible, separation of mock and native tests.
5. Profiling results with the same game scene before/after; the value of the average/p95/p99 frame and the number of processed/delayed events.
6. Results of save/load and migrations; separately indicate the status of the old warm-load `0xC0000005` (do not declare it fixed without checking).
7. `KNOWN_LIMITATIONS.md` - list of features not included in V1; `ROLLBACK.md` - safe shutdown/rollback procedure.
8. Update the project index and documents, but **do not delete historical documentation**.

**If the real environment is not available:** honestly indicate “a patch/code has been prepared, NOT installed and NOT tested in the game”; do not assert functionality, do not simulate test execution.

---

## 14. Stopping rule and minimum success

If the full concept of V1 is too big, **don't go into a whole country pseudo-implementation**. Make and prove the sequence:

> existing NPC → location-independent queue of events → work and consumption → saving → changing the priority goal → searching for a vacancy → changing profession → saving/loading → observed correct state when the player appears.

After that, expand to one group of NPCs, relationships and news about events. This is the minimum useful core that can be developed while the author of the project adds transport and locations.

**V1 cannot be declared ready if NPCs simply gain random new stats once per day, if they are frozen when leaving a location, or if events create items/money without verified operations.**

---

## 15. Separate directions for V2+ (in V1 just prepare the API)

- Full elections/legal political career with real NPC and player competition.
- Families, relatives, children, social inheritance, transactions and home ownership.
- Companies, resource economics, industry, factory employment and markets.
- Long-term modeling of leaders, organizational diplomacy and conflicts.
- Real life of doctors, drivers, utilities, educational institutions.
- Integration of unique discoveries, including the Gustav bunker, with real coordinates, technical condition, ownership and consequences in the laws of NChG.
- Real online with server authority; The offline NPC simulator should remain a separate controller so that the rule logic can be reused.

---

## 16. Exact starting request for another AI

> Open `D:\CCZMP PROJECT` and read the attached `CCZMP_AUTONOMOUS_LIFE_V1_TECH_SPEC_RU_2026-10-28.md`, then the full audit of `CCZMP_PROJECT_FULL_REPORT_2026-10-28.md`. Don't start by rewriting `cczmp_life.script` blindly. Check current Lua/LTX, existing UID/ALife/banking/organizational/dispatch APIs, save/load, create backups and integration map. Implement a working V1 event-based autonomous life for NPCs, regardless of the player’s location, starting with 10–30 existing citizens and expanding the functionality beyond the native acceptance testing. Don't create a parallel fictitious balance/ownership/investigation and don't consider a mock test to be sufficient. The result is installed patches, tests, logs, profiling, rollback instructions and an honest report.

---

**Note on Sources:** Source facts from CCZMP audit 10/28/2026, sections 2-7 and SYS-01, 03, 06, 10-13, 19, 35, 45, 50-56, 58, 73, 78-80. The architecture, API schemas, events and test plan in this document are **new design proposal** and are not asserted to exist in the code.
