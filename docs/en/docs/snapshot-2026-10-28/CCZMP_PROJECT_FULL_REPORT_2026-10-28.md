[Русский](../../../snapshot-2026-10-28/CCZMP_PROJECT_FULL_REPORT_2026-10-28.md) · **English** · [Documentation index](../INDEX.md) · [Translation notes](../../TRANSLATION.md)

# STALKER X CCZMP - full report on the status of the project

> Historical audit until completion of Autonomous Life V1. Current clarifications for 22 residents, banking adapter and public modules: [status](../STATUS_EN.md), [current register](../SYSTEMS_EN.md), [change history](../CHANGES_EN.md). Below are the findings at the time of the audit.

**Date:** October 28, 2026, Asia/Qyzylorda.  
**Working base:** S.T.A.L.K.E.R. Anomaly 1.5.1 / X-Ray, `D:\CCZMP PROJECT`.  
**Additional component:** `D:\CCZMP PROJECT SITE`.  
**Purpose:** return a clear picture of the project and convey to the developer/AI verifiable boundaries of what is done, what is unfinished and what is planned.

## 1. Main conclusion

The project is already a large **offline prototype of interconnected city systems**, and not just a set of models or lore. There are government procedures and documents, virtual electronics with accounts, a bank, a workshop and medicine, transport, taxis, exits IC and 111, limited NPC life, a criminal area, real deliveries, towing, reputation and local infrastructure. Separately, there is a modular site with a permanent forum and SQLite.

At the same time, **a complete simulation of the population, a material industrial economy, real estate, all the special mechanisms of technology and a general multiplayer world have not yet been created in the scope of a large concept**. The presence of a menu, OGF, section, organization or program does not mean that the associated life/production cycle is complete.

It is impossible to honestly name one percent of the project’s readiness: the concept contains directions of different scales, and checks have different depths. Neither the number of files nor the sum of old tests serves as such a percentage. The implementation, confirmations and remaining result are listed separately below.

## 2. What exactly was checked in this audit

Available old and new documents from the project folder, existing `docs`, loads user on C: and a separate site project were checked. Read texts and tables, unpacked ZIP document attachments; For the only PDF found, all 18 pages with transport distribution were extracted. A separate parsing was used for the PDF because the original remote viewer did not open it. Documents in this chat's applications are mapped to work materials.

Old versions are not deleted or rewritten as if they always described the current result. Exact repeats are merged using SHA-256, preserving all original paths. The content and encoding of the originals did not change. New found documents have been added to `docs`; The game code, save code and forum database have not been changed.

Additionally, we read the current Lua/LTX, lists of `gamedata` models, saved JSON test results, logs of native runs, part of the installation manifests and site code. The site's SQLite is read-only; account contents, passwords and session secrets are not included in the report.

**New full in-game acceptance testing has not been run at this time.** The phrases "tested in game" below refer to the specific historical results found, and "in code" refers to the current contents of the files. An old successful test is not declared a successful retest of all subsequent changes.

### 2.1 Check numbers and their meaning

| Indicator | Snapshot | How to understand |
|---|---|---|
| Unique project files in parsing | 371 | 98 text documents/notes, 16 technical appendices, 8 tables, 6 HTML, 241 licensed material and 2 registers. |
| Original Entries/ZIP | 1395 / 262 | Repetitions are not destroyed: their paths are preserved; the number of ZIPs is not equal to the number of ready-made models. |
| CCZMP scripts | 90 files: 88 regular + 2 profile probes | Not the number of independent complete subsystems. |
| Organizations | 41 | Current in-game registry; individual bases/forms/cycles are not guaranteed. |
| Main catalog of items | 197 entries | Donor and other specialized sections are considered separately. |
| Application Catalog | 51 entries | Not all applications have a unique UI/complete independent E2E. |
| Donor directory | 246 entries | One source scene can produce several entities; There are different classes and sets. |
| Transport sections with OGF | 85; missing OGF: 0 | 76 available catalogs + taxis + 4 drones + 4 services. The existence of a resource does not equal sea trials. |
| Disabled transport cards | 11 | Empty sections/available=false; not included in 85. |
| All loose OGF in gamedata | 508 files | Includes staff/static/subject/variants; not 508 unique gaming machines. |
| Website | Flask + SQLite + frontend | Local implementation is confirmed by files and database structure, not public operation. |

The difference between 34/38/41/42 organizations in the documents does not need to be corrected by arithmetic: 34 - early game registry, 38 - coverage of the proposed PDF transport, 41 - current game registry, 42 - site content lines. These are different dates and samples. The site does not prove the presence of 42 full-fledged institutions in the game.

### 2.2 Meaning of statuses

- **Tested in selected scenarios:** There are specific native or described test results, but not a statement of any conditions.
- **Partially:** useful mechanics already exist, but the concept is broader or significant untested branches remain.
- **Prototype:** resource/class/base behavior created, unique mechanics and acceptance testing not finished.
- **Code / needed acceptance testing:** function found, but a full user loop has not been confirmed.
- **technical specification / implementation not found:** there is a goal/contract, but a complete game loop was not found in the tested composition. This is an inference about the materials available, not a proof that such code cannot exist elsewhere.

## 3. What can already be presented as an existing result

### 3.1 Foundation and government procedures

The F6 terminal and F7 extensions, real community organizations and positions with rights, subject passports/IDs and permanent identities work. Corrections to documents and contacts PDA are supported by separate checks of return input, buttons and F6/F7. State actions check not only the UI button, but also the authority, purpose, distance and required stage of the case.

There is a chain of “case → prosecutor’s office → court → warrant/decision → execution,” separate arrest and search warrants, detention/convoy of regular NPCs, fines/debt and a logical period of detention. More recent systems have added physical seizure with proof of transfer, protocol, paddy wagon, evidence history, and suspicion/proven event distinction. Based on the native result found, the NPC was actually planted and delivered, the item was actually received, and the re-seizure was rejected.

An automatic investigation is no longer just an idea: there is a witness, transmission of testimony, departure IC, examination of the body, documents/devices as real materials and news. But this is a limited gaming algorithm and route set, not an omniscient legal AI.

### 3.2 Devices, network, apps and money

The phone/PDA/PDA/laptop retains its UID, charge, OS, SIM, programs, messages, files, parameters and session. Someone else's unlocked device does not become the player's property when the window is opened; operations use the active session account. There is an official store, F-zondroid, a set of virtual network tools and .nchg services. A later package added separate native screens and the City NChG app.

The NBZ now has a separate balance, deposits/withdrawals, transfers between citizen keys, deposits/loans and blocking. Therefore, the phrase in the certificate dated 08.10 “there are no separate accounts/transfers” is outdated. This is still a personal gaming bank: it does not imply a ready-made corporate ledger, ministry budget, stock exchange or tax platform.

Remote loss/blocking of the device, recall of sessions, one-time recovery and saving of correspondence were tested in the city stage. At the same time, a full-fledged audio call/FPV did not appear from the presence of interfaces.

### 3.3 Items, workshop, medicine and crime area

There is a subject catalog, materials/tools, saved operations, skills and recipes; code cases and master keys; real artifacts in the container; licenses/prescriptions and dose consumption; diseases and treatment, tourniquet, defibrillator live critical NPC; ammunition and protection with wear. Donor weapons have been moved to in-game bases with HUD/world models, including Operator and Vandal.

The southwest region of Dead City has ten permanent members, two companies, a middleman, a shop/buyer, real budgets and inventories, two final deliveries, a mechanic's debt history, extortion, and a call to MVD/IC. The reboot should not create a new checkout or replace the original load with a debug copy. This area already provides a limited social-criminal game cycle, but not a war of all OCG for enterprises.

### 3.4 Transport and city services

The base W140 has particularly specific evidence of spawn, controls and cold loading; the ground base includes the engine, fuel, damage, trunk and service operations. Separate tank tests confirmed curb, player armor, HE/AP, smoke/explosion, and occupied tank recovery. This is not an automatic acceptance testing of each donor body.

Eight previously absent cars were indeed rescheduled on 10/18. Four drones received physical flying sections. 10/22 added 25 more separate OGFs from 24 archives, including the sedan/wagon division: 23 transport sections and two world objects. Therefore, the result of October 17 about “46 cars and eight not yet transferred” is no longer relevant.

The 111 service has a queue, priorities, application history, ambulance, police, OMON and a paddy wagon; four own service options. The first geography is Dead City. Seated crews use built-in models tied to real ALife NPCs: this is a bypass of CCar restrictions, not a full-fledged general passenger engine system.

The taxi has route data for 23 locations and an estimated fleet of 69 W140s; local travel and payment were checked separately. These are not inter-location flights and are not proof of the smooth operation of each route. The ZonaTaxi application uses existing transport, but a complete user order through it remains a separate acceptance.

### 3.5 Urban connectivity

In the city stage there is a transport register and permits, real parcels with payment upon receipt, repair orders with the consumption of materials, three nodes of local infrastructure and a separate reputation of the witness/district/organization. Positive results were found for delivery, failure with a dead recipient, state restoration, communication repair and one-time reward.

Physical towing was confirmed: the car traveled 25.05 m, the truck 25.93 m, the coupling/uncoupling worked. A full order of evacuation to an impound lot and an independent driver-tow truck are not proven by this.

The life of an NPC is currently limited to a small pilot of three employees: schedule, trust, hunger/fatigue and memory with preservation. There are other patterns of patrols/witnesses/services, but there is no statement of a complete biography of each resident.

### 3.6 Website

`D:\CCZMP PROJECT SITE` contains frontend, Flask backend, SQLite, schema and tests. The database contains users, categories, boards, topics, posts, login_attempts, factions, news; content - four categories, nine threads, 42 faction entries and five news. There are no topics/posts in the picture: the forum layout exists, but this does not prove that the community is full.

The code supports parameterized SQL queries, scrypt for passwords, CSRF/roles, and secure forum text insertion. No new independent security or browser-based acceptance testing testing was performed in this audit. HTTPS publishing and a number of custom features remain a work in progress.

## 4. What exists, but cannot be considered finished yet

| Direction | Made part | Unfinished |
|---|---|---|
| New donors 22.10 | 25 individual OGFs; two machines physically created and coldly restored | Test every vehicle, no_place near the bus/Ka-52/Su-30; warm loading was falling. |
| Aviation | Mi-2 and prototypes based on it | Aircraft physics, rotors/cockpits/combat functions and proven flights of new types. |
| Trains, buses, special equipment | Models and General Physics Sections | Rails/couplings/walking, passengers/doors/joint, crane/air defense/working parts. |
| 111 and taxi app | Queues, routes, crews, part of native scripts | Full consumer path, combat/overload, crashes and all maps/interrupts. |
| Real estate and businesses | Lore and role records; transport property | Homes/rental/corporate assets and property economics are still separate. |
| NPC Life | Three profiles, local schedules/memory, dedicated AI services | Autonomous life, families, work/property and social destinies of the entire population. |
| Engineering | Recipes and local repairs | Physical circuits/instruments and industrial process technology. |
| Right | Procedural flow and real actions | Full prison, appeal, harmonization of standards and all cases of evidence. |
| Voice acting/animation/look | Some textures, sounds, UI and reused animations | Film animation of the document, doors/shield, full voice acting/LOD/renders. |
| Forum | Persistent database and main API | Public deployment, password recovery, attachments, notifications and independent acceptance testing. |

## 5. What else remains to be implemented according to the big concept

1. **Material Economics and Industry.** Final deposits/exploration, raw materials batches and origins, BOMs and production orders, machine tools/capacity/scrap, component factories and assembly, contracts/warehouses/logistics. A subject workshop and the repair of three units do not replace this.
2. **Corporate property.** Legal entity, enterprise as a property complex, shares/shares, land/license/machine as various rights; acquisition, sale, donation, lease, reorganization and inheritance.
3. **Financial platform.** Unified transactions/balances, corporate accounts, budgets/salaries, taxes, escrow, liabilities and bankruptcy. Personal transfers already exist; this entire block does not follow from them.
4. **Complete infrastructure.** Energy generation and networks, water/sewage/heat, enterprise loads, ZONASTROY construction with physical facilities and reception. Now there are gaming logic nodes and local device communication.
5. **Automotive industry NChG.** Product design → components/origin → prototype → testing/certification → series/VIN → dealers. NAZ is named as the author; VAREON, NEOTERRA, PEOPLE, VARGAN, AVTOMIR/AVM in technical specification are working options, not automatically approved by concerns.
6. **Housing and public spaces.** One realistically accessible property with owner/lease/rights/storage as the first cut; then apartments, dormitories, warehouses, pick-up points, garages, houses, offices, shopping centers/stations/depots and departmental interiors.
7. **Autonomous life of the population.** General rules for work/money/property for NPCs, relationships/families/debts/lodging, goal planner, changing professions, life events, long-term memory and controlled background simulation.
8. **Education and professions.** Not just a few skills/services, but universities/colleges/curricula/practice/exams and 100+ different completed work cycles.
9. **Native special transport mechanisms.** Rail movement and couplings, carriage walking, passenger doors/seats and bus articulation, aircraft aerodynamics, air defense/crane/logging equipment, water transport buoyancy.
10. **Full procedural and prison system.** Closed premises, physical confinement of the player, all stages/participants of the hearing, appeal with reversal of consequences, agreed upon rules of punishment and departmental supervision.
11. **Plot and setting.** The old combined scenario is not a realized campaign. Need game episodes/resources/triggers and acceptance testing; the choice between story progression and free life remains the goal.
12. **One life.** A new character/personality, the fate of property/debts/organizations and death from a bug require their own rules and code. Regular death or Ironman Anomaly mode alone do not close the CCZMP's vision.
13. **Unified online.** Reputable game server, two clients as the first experiment, synchronization of items/transport/rights/money, interest management and load checks. One official logical world and 1000–2000 players are the architectural goal for now. The backend of the forum is not a game server.

ZONASTROY, ChernEnergo and ComNet already have entries/roles and separate game actions; Full-fledged companies with industrial assets do not follow from this. Discrepancies between ZONASTROY/MonolitStroy and individual canonical names in the original concepts should be resolved by the author; audit does not rename them.

## 6. Contradictions between old and new materials - resolved statuses

| Old statement | Late confirmation | Audit summary |
|---|---|---|
| 17.10: eight cars missing | 10/18: 203–210 established/described; current models exist | The old list of absentees is closed; assess the current readiness of each machine separately. |
| 17.10: drones only items | 18.10: fa_042–045, physical flight/control and results | The flight has appeared, the FPV video channel is still missing. |
| 08.10: bank - wallet, no transfers | 15.10 and code: account_state/transfer/cash_account | There are personal accounts/transfers; the corporate platform is not ready. |
| 08.10: no autonomous investigation/transport of prisoners | 15–19.10: departure IC, 111, paddy wagon, procedure/native results | The general status “not implemented” cannot be maintained; specific limits remain. |
| 10.10: aircraft prototype not added | 10.11 and later: Mi-2 and new resources | There is a manned prototype; full-fledged aviation of all types is not ready. |
| Early Radio: Track First/Sound Off on Exit | Later broadcast by seconds and saved state | Apply late broadcast rather than the old player restriction. |
| 16.10: tank - stand only | 16–18.10: tank_nchg and native in-game checks | The tank exists; the stand is not equal to proof of work of the entire heavy park. |
| The site is an old HTML monolith | Separate CCZMP PROJECT SITE: backend/database/frontend | There is a local permanent forum, but production publishing has not been proven. |
| 23.10 worklist: new “source” models | The current native_section/OGF and package 22.10 are already there | The queue reflects the acceptance testing requirements, but not a reliable list of missing models. |
| Document22.10: persistence not yet confirmed | Late log: two cars/two contracts restored | Narrow cold-case confirmed; Warm crash remains a separate problem. |

### 6.1 Saves and crash October 22

In `STATUS_RU.md`, an access violation `0xC0000005` was recorded when attempting loading in the same process. In `native_live.log` after this there is a **positive separate recovery**: 23:55:07 - both entities `cczmp_fv_242` and `cczmp_fv_230` are present and online, `car=true`, two contracts are restored, `RESTORE_PRIVATE_COMPLETE 2` is recorded.

Therefore, the correct conclusion is: **cold recovery of two specific machines is confirmed; warm crash is not explained and the overall persistence of the entire package/85 sections is not accepted**. The absence of fatal markers in one main `appdata/logs/xray_user.log` does not cancel the failure of a separate test profile.

For the urban stage, the early unfinished output is also clarified: `native_loaded_verification.json` contains call recovery, driver, notes, SMS/settings/taxi history, holder removal and completed delivery. This is a confirmation of a specific scenario after loading, not any battle/interruption/number of crews.

### 6.2 Manifests and current status

City Pack: 25 out of 25 files checked match `installed.json`. Donor package 10/22: 558 are the same, 25 OGF are different, no missing files. All 25 of these models are listed in the following `visual_repair_installed.json`: differences are consistent with later redesign and do not automatically indicate damage. But the original installed manifest is no longer an accurate description of the current bytes and requires updating.

Package 18.10 had 325 files matched, 11 common scripts/configs were changed by subsequent stages, and there were no missing files. You cannot restore an old package on top of a new one, ignoring other people's changes. The rollback must remain tied to its stage.

There are two `zzzz_cczmp_*_owned.script` left in `gamedata`. Their security has been verified: they only register test actions for their own `tools/.../native_appdata`, so the mere presence of files does not prove interference with a regular profile. Before public packaging, they should still be excluded from the release composition and teardown checked separately.

## 7. Recommended work queue

The priorities below are a proposal based on the audit result. They do not change the author's intention and are not a completed implementation.

### P0 - fix stable composition

1. Reproduce the 22.10 warm crash on a copy, get the cause/stack and a verified fix or explicitly supported limitation. Don't declare it the same corrected old `clsid`/`save_state` just because of a similar symptom.
2. Commit a new holistic manifest after visual repair, a list of modules, config/save versions and a set of test saves.
3. Repeat the general user cycle on the current composition: document → closing → item → F6/F7 → gadget → trunk → boarding/exit → saving → new process → loading.
4. Clean installation and loading old/new save; User saves for tests should not be used as the only copy.

### P1 - complete one linked city

1. Take all the way 111: call → queue → actual departure → crew exit → assistance/check/detention → delivery → return; separately death/interference/no road/reboot.
2. Go through the ZonaTaxi order through the application from selection to payment/exit and restore the trip in the middle.
3. Accept city order/actual cargo/trunk/payment along with case, permit and reputation. Then complete the evacuation to the impound lot.
4. Select a small mandatory fleet for the first release and accept each model: visual/collision, landing/camera, controls, light, trunk, damage/death, save/load. It’s fair to leave the rest as prototypes.
5. Then add **one** premises with owner, rent, access and storage - this is the missing part of the original S2.

### P2 - fine-tuning the existing

Update references for the current code; agree on articles and powers; close audio/interface/zoom; check the right to issue equipment to each organization; optimize the heaviest OGF/textures/LOD; complete custom forum features and public configuration. What is needed is a reproducible set of regressions, not a summation of old PASSes.

### P3 - major new platforms

It is reasonable to start the material economy using a ready-made technical specification with one complete slice: final resource → extraction → batch → delivery → production with energy/time → product → sale/transfer of rights → cold loading without duplicates. After that, expand factories/industries. NPC planner, walking train, airplane aerodynamics and online are separate projects with their own criteria acceptance testing.

## 8. Criteria after which a subsystem can be called complete

For a specific agreed volume, the following must match: available user input; correct verification of rights/conditions; real game result; double action limitation; saving/restoring and loading old moment; death/deletion/change of level; no new fatal/runtime errors; reproducible evidence; instructions/restrictions; current manifesto and rollback. Unique mechanisms are tested on their own model rather than derived from a legacy class.

The “system implemented” indicator should be stored along with the version, date, boundaries and evidence. If there is only a model, catalog entry or design stand, the status remains appropriate. Changing the common module after checking forces the affected scenarios into re-regression.

## 9. Detailed register of all directions

The register has 80 lines: for each, the result, the unfinished part, the basis and the proposed priority are separately indicated. This is not 80 tasks of equal size and not a denominator for the percentage of completion.

### Basic

| System | Status | What already exists | What's left/foundation |
|---|---|---|---|
| SYS-01 Offline build Anomaly 1.5.1 | Partially | There are working game modules, configs, resources, interfaces and saved native in-game checks. | General acceptance testing of all current package combinations; clean install and long-term regression. [P0]; S001; S071; S074; S075; CODE:gamedata/scripts/cczmp_runtime.script |
| SYS-02 Windows, F6/F7, control return | Tested in selected scenarios | Terminal, documents, gadgets, radio, certificates, trunk; transitions and removing your own input capture. | Regression after all new packages, different resolutions, death/deletion of target/change of level. [P1]; S061; S075; E:tools/ui_fix_work/verification_result.json |
| SYS-03 Persistent Identity and Serialization | Partially | UID of things and persons; ALife storage, ID+name/section checks, pending operations; individual cold loading confirmed. | Combine migrations into a single contract and close the matrix of all subsystems/old saves. Warm crash package 10/22 is not explained. [P0]; S074; S324; S370; E:tools/donor_import_20261022/native_live.log |
| SYS-04 Backups and Rollback | Partially | Stages have baseline/installed, protected hashes and rollback with checking other people's changes. | Rebuild the current manifest after visual repair; try installing/rolling back the full release package on a copy. [P1]; E:tools/city_systems_20261019/installed.json; E:tools/donor_import_20261022/visual_repair_installed.json |
| SYS-05 Source and Dependency Index | There is data / need updating | Old INDEX and connection graph, paths to modules and resources. | Rebuild the index after modifications 18–23.10; The old number of files should not be considered current. [P2]; S000; S003; S312; S318; S321 |

### State

| System | Status | What already exists | What's left/foundation |
|---|---|---|---|
| SYS-06 Organizations and native communities | Partially | 41 organizations in the current factions.ltx; membership, positions, relationships, rights and debug spawn. | 41 records do not mean 41 completed departmental cycles, bases and vehicle fleets. Check all ranks/issues/connections. [P1]; S001; S002; CODE:configs/cczmp/factions/factions.ltx |
| SYS-07 Passport, ID, identity register | Tested in selected scenarios | Items and owners, full name/portrait/number, viewing, validity of ID, link to dossier, preservation. | Re-issue of the lost document and calendar aging have not been confirmed; not all departments have a separate complete set. [P2]; S061; S001; E:tools/ui_fix_work/verification_result.json |
| SYS-08 Animation of presenting documents | technical specification / no implementation found | There are objects, textures and a viewing screen; SVG identity concept IC. | Physically retrieve, open, show and remove a document from a first/third person perspective; similar actions of NPCs. [P3]; S062; S063; S005 |
| SYS-09 Criminal Code, Administrative Code and financial rules | Partially | Texts of regulations and gaming sanctions, powers, fines, debt, terms and orders. | Reconcile clause/rule variances, NPC repetition, property requirements, and full coverage of original proposals. [P1]; S001; S002; CODE:configs/cczmp/law |
| SYS-10 Investigation → prosecutor's office → court | Tested in selected scenarios | Cases, roles of the author, materials, transfer/return, orders, calculation and confirmation of the decision with the judge. | An autonomous meeting with full procedural roles and assessment of all types of evidence is not ready. [P1]; S059; S324; E:tools/gadget_dispatch_20261019/native_procedure_result.json |
| SYS-11 Automated Murder Investigation | Partially | Witnesses/visibility, limited identification, team IC on W140, body inspection, physical materials, news. | Drive through complex branches: no road/witnesses, masks, dead crew, several places, level transitions; expand geography. [P1]; S022; S324; CODE:cczmp_investigations.script |
| SYS-12 Evidence and Transfer History | Partially | Source, quality, custodian, transmission, weather deterioration of open traces, packaging; independence of witnesses. | Close E2E on contradictions, false indications, all types of physical traces and preservation at every transition. [P1]; S324; CODE:cczmp_city_model.script |
| SYS-13 Detention, search, seizure, paddy wagon | Tested in selected scenarios | Protocol, separate search warrant, actual transfer of item, re-seizure defense, NPC boarding/delivery. | Restrictions on story NPCs and resistance remain; full player prison and all branches of enforcement are not confirmed. [P1]; S324; E:tools/gadget_dispatch_20261019/native_procedure_result.json; E:native_loaded_verification.json |
| SYS-14 FSIN and physical prison | Partially | There is a logical point of containment, deadline, retention/release of NPCs; paddy wagon as transportation. | Locked cells, interiors, full facility mode, labor/regime and physical confinement of the player. [P3]; S001; S059; S324 |
| SYS-15 Appeal and Reversal | technical specification / no implementation found | Justification and cancellation of active orders exist in their own threads. | A complete review of the entered decision, return of the collected fine and cancellation of all property/service consequences. [P2]; S001; S002 |
| SYS-16 Departmental Bases and Maintenance | Partially | Rostock site pilot, base/employees IC to Dead City, job roles and appeals. | Separate verified databases of all institutions, interiors, premises and maps according to a large concept. [P3]; S059; S022; S005; CODE:cczmp_deadcity.script |

### Communications and gadgets

| System | Status | What already exists | What's left/foundation |
|---|---|---|---|
| SYS-17 Physical Devices with UID | Tested in selected scenarios | Charge, OS, SIM/tariffs, locks, memory, programs, files, contacts, settings and sessions belong to the subject. | A separate complete visual model of each brand, resource limitations of all combinations and long-term scenarios. [P2]; S019; S022; S326; E:city_native_result.json |
| SYS-18 Application Interfaces and Stores | Partially | Native CUI, official store, F-zondroid, compatibility, memory, purchase and installation; 51 catalog entries. | 51 entries does not equal 51 independent, fully verified applications; professional programs use a common layout. [P2]; S022; S326; CODE:cczmp_app_catalog.script; CODE:cczmp_app_views.script |
| SYS-19 Messages, calls, contacts | Partially | In-game address communication, history, text questions/answers, tariffs; correspondence restored after loading. | Full audio calling, voice multiplayer, and random conversational AI have not been confirmed. [P2]; S022; S326; E:native_loaded_verification.json |
| SYS-20 Public services and personal profile | Partially | Citizen account, documents, position, affairs, debts, search, personal transport. Missing taxes are not made up. | Full tax/social accounting, unified corporate register and all government services of a large concept. [P2]; S326; S324; CODE:cczmp_gov_profile.script |
| SYS-21 Remote device protection | Tested in selected scenarios | Lost/banned, session revocation, PIN/one-time recovery, history and botnet connection. | Extended regression of owner rights, loss of control equipment, offline objects and old saves. [P2]; S324; E:tools/gadget_dispatch_20261019/city_native_result.json |
| SYS-22 In-Game Networking and Hacking | Partially | Virtual services .nchg, scanning, protection/ports, tasks, files, decryption, botnet, interference, audit of operations. | Content/balance expansion and native regression of all tools. These are game simulations, not a full-fledged OS/external network. [P2]; S019; S022; CODE:cczmp_electronics.script; CODE:cczmp_hacking.script |
| SYS-23 Radio “Voice of Pripyat” | Tested in selected scenarios | General broadcast by seconds inside saving, music/inserts, radio of the world/car/PDA, saving switching on and position. | Content of special stations, quality and rights to recordings; independent bypass of maps and DX modes; There is no network synchronization. [P2]; S066; S067; E:tools/radio_air_work_20261010/installed_audit.json |
| SYS-24 Voice acting for organizations | Partially | There are texts and cue connection points, radio inserts and service signals. | Full voice acting of dialogues and ready-made unique replicas of all organizations have not been confirmed; playback scripts and acting recordings. [P3]; S008; S066; CODE:cczmp_voice.script |

### Items and engineering

| System | Status | What already exists | What's left/foundation |
|---|---|---|---|
| SYS-25 Item Catalog and Trade | Partially | 197 entries in the main items catalogue, real items/supplies, tools, materials, medicines, equipment and donor items separately. | Full compliance with all source PDFs and unique visual models; prices and assortment require balancing. [P2]; S019; CODE:configs/cczmp/items.ltx |
| SYS-26 Workshop, skills, recipes | Tested in selected scenarios | Time, tools, material consumption, experience/approvals; repair, assembly of devices and kits. | Physical workplaces and full-fledged technological processes of factories; end-to-end material accounting. [P2]; S019; S024; S035; CODE:cczmp_engineering.script |
| SYS-27 Measuring instruments and instrumentation | Partially | Devices as objects/conditions of operations; gaming diagnostic actions. | Physical measurements of real circuits, oscilloscope waveforms, calibration, benches and deep automation. [P3]; S019; S005; S006 |
| SYS-28 Cases, combination locks and master keys | Tested in selected scenarios | PIN, limits, locks, initial items and pending transfers, saved opening operation. | Linking to doors and locks of physical buildings; full subject animation. [P2]; S019; S024; S073 |
| SYS-29 Artifact Container | Tested in selected scenarios | Transfer of real two artifacts to a hidden container, weight and condition, sales bonus. | Physical cooling/nutrition; additional native checking of map transitions. [P2]; S019; S072 |

### Medicine and weapons

| System | Status | What already exists | What's left/foundation |
|---|---|---|---|
| SYS-30 Diseases and Medical Actions | Partially | Game disease states, recipes/dosages, tourniquet/gangrene, specialized specialists, defibrillator for live critical NPC. | Balance and all disease/treatment combinations; graphics and full hospital/operations of a large concept. [P2]; S019; CODE:cczmp_medicine.script |
| SYS-31 Licenses and Recipes | Tested in selected scenarios | Physical form + owner + admission record, categories A/B/C/D, certificate IC, recipe and limitation of use. | Remaining legal scenarios, re-release and full coverage of original legal proposals. [P2]; S008; S019; CODE:cczmp_licenses.script |
| SYS-32 Ammunition, armor, shield, special equipment | Partially | Real packs, ammo options, head/body protection, wear, heavy equipment restrictions, gas/taser. | Author's animations of the shield/hands, visual refinement of sets and balance of all combat combinations. [P2]; S019; CODE:cczmp_gear.script |
| SYS-33 Donor weapon | Partially | 7 weapon entries from the donor catalog; game databases and HUD/world models, including Operator and Vandal. | Check each set/option and state transitions separately; own animations and accuracy of real performance characteristics have not been confirmed. [P2]; S325; CODE:configs/cczmp/donor_catalog.ltx |

### Characters

| System | Status | What already exists | What's left/foundation |
|---|---|---|---|
| SYS-34 Forms and models of organizations | Partially | 7 native/state options, special forces rank package; 6 donor NPC records, including SChS. There are game promotion/demotion checks. | Unique, accurate uniform/equipment for each department and rank; rights to distribute individual packages. [P2]; S064; S298; S325; E:state_uniforms_20261009/verification_result.json |

### Transport

| System | Status | What already exists | What's left/foundation |
|---|---|---|---|
| SYS-35 Basic Automotive System | Tested in selected scenarios | CCar, engine/fuel/damage, purchase/rent/issuance, GPS, blocking, physics and saving individual cars. | Individual finishing and complete acceptance testing of each body, interior, entry/exit; LOD and large vehicle fleet. [P1]; S019; S056; S330; CODE:cczmp_transport.script |
| SYS-36 New models October 22 | Prototype | 25 OGF: 23 transport sections and 2 world objects; file/sections/materials are present, 25 sections are recognized in the test. | driving tests all machines; for bus/airplane there is no_place; 2 cars were restored cold, the warm crash was not explained. [P0]; S370; S342; E:tools/donor_import_20261022/native_live.log |
| SYS-37 Tank NChG | Tested in selected scenarios | Physical rollers/drive, turret/ammo, HE/AP, damage/armor, curb and cold loading in tests. | Finalization of the hull/chassis/controls, a full fleet of heavy vehicles, all renderings and a long stress test. [P1]; S048; S330; E:tools/vehicle_fix_20261017/final_verification.json |
| SYS-38 Mi-2 and new manned aircraft | Prototype | Mi-2 with holder/flight; Rafale, flying motorcycle, Ka-52, Su-30/Su-27 models use a common base with settings. | Aircraft aerodynamics, own controllers/cockpits, Ka-52 rotors, proven flight of new models. [P2]; S045; S370; CODE:cczmp_aircraft.script |
| SYS-39 Remote DJI/Shahed | Partially | 4 physical devices, launch from an object, control from the ground, charge/communication/reconnaissance, collection/destruction, saved native data. | FPV video channel and device camera; unique aerodynamics/animations, enhanced acceptance testing of all profiles. [P2]; S325; E:tools/donor_completion_20261018/native_drones_final.json |
| SYS-40 Trains and subways | Prototype | EMD GP7, Alstom Metropolis, InterCity 125 have been moved to physical automotive sections. There is a path/station as objects. | Rail controller, couplers/pointers/signaling, routes and free walking inside moving cars. [P3]; S328; S329; S005; S071 |
| SYS-41 Bus and Passenger System | Prototype | Volvo 7900A as resource/section; Taxi and service transport have their own limited schemes. | Articulation, doors, passenger seats, interior and general NPC passenger CCar; testing of the bus itself has not been completed. [P2]; S326; S370; S342 |
| SYS-42 Cranes, logging and air defense | Prototype | KS-4574/5363, CAT, Tor-M1 and static Liebherr are represented by resources/transport or object. | Lift/load, CAT working parts, radar/SAM Tor; a regular W140 frame does not cover these mechanisms. [P3]; S040; S325; S370 |
| SYS-43 Gustav | Prototype | Stationary installation, stock of shots, direction/range settings, hit simulation. | Real heavy projectile, railway movement, separate installation mechanisms. [P3]; S040; CODE:cczmp_emplacement.script |
| SYS-44 Ural PES-4320 | Source / non-game resource | There are technical Blender models V04/V07 and preparatory materials. | Game optimization, skeleton/collision/OGF, power generator, interaction and acceptance testing; Ural was not found in the current gamedata. [P3]; S046; S052; SNAPSHOT:gamedata/meshes |
| SYS-45 Taxi and ZonaTaxi | Partially | Routes/geometry at 23 locations and 69 planned vehicles; payment and physical travel were checked separately; the application books the W140. | Full custom order via app, traffic jams/obstacles and cold loading on all maps; There are no interlocation flights. [P1]; S047; S051; S326; E:tools/taxi_world_20261015/verification.json |
| SYS-46 Trunk and real things | Tested in selected scenarios | Two inventories, original items/UID, linked container, no re-transfer, restore from save. | Weight/volume limit, cover, destruction/removal of the machine, full-fledged interlocation acceptance testing of all models. [P1]; S008; S066; E:tools/trunk_gadgets_work_20261010/final_verification.json |
| SYS-47 Machine Registry and Access | Partially | Owner/agreement/number, key permission, power of attorney, transfer of property, theft/search and access to controls/trunk. | Physical model of the key, all transfers/disputed rights, liens/insurance and a complete unified property register. [P2]; S324; CODE:cczmp_city.script; CODE:cczmp_transport.script |
| SYS-48 Towing and Recovery | Partially | Spring with damping and opposing forces, coupling/uncoupling; in fact, about 25 m have been covered. There is an order for evacuation/penalty parking. | Full native route to the impound lot and an independent NPC tow truck; acceptance testing all trucks/combinations. [P2]; S324; E:tools/gadget_dispatch_20261019/native_towing_result.json |
| SYS-49 Lights, sirens, city sound | Partially | Lights/lenses and rear red sources, G horn, organizational sirens, background and clearing sounds when subject leaves. | The entire fleet/all DX, geometric fine-tuning of new bodies, full-fledged flashing lights and unique equipment by department. [P2]; S054; S330; CODE:cczmp_vehicle_lights.script; CODE:cczmp_vehicle_audio.script |

### Town and NPCs

| System | Status | What already exists | What's left/foundation |
|---|---|---|---|
| SYS-50 Dispatcher 111 and crews | Partially | Applications, priority/queue, ambulance/police/OMON/paddy wagon departure, status and history; 4 separate service sections. | The first stage is limited to the Dead City; no guarantee of arrival time, full fight OMON/all departure branches are not closed. [P1]; S326; S324; CODE:cczmp_emergency.script; CODE:cczmp_response.script |
| SYS-51 Transportation of crews and detainees | Partially | Built-in seated models linked to real ALife NPCs, exit/return and delivery; restoration of part of the transportation is verified. | This is a workaround for the CCar limitation rather than a generic native multi-passenger system; we need to fine-tune all interruptions. [P1]; S326; E:tools/gadget_dispatch_20261019/native_loaded_verification.json |
| SYS-52 The life of three employees IC | Tested in selected scenarios | Personality, schedules, needs, trust and 12 memories; background limited calculation; native cold loading. | Needs do not yet consume food and do not harm health; it is not the life of every NPC, nor is it a socio-economic planner. [P2]; S074; S075; CODE:cczmp_life.script |
| SYS-53 Complete autonomous life of the population | technical specification / no implementation found | There are separate profiles, AI schemes, witnesses, service roles and local reactions. | Families/divorces/housing, autonomous job changes, careers, NPC business, life goals and a large social graph. [P3]; S005; S074 |
| SYS-54 Crime Area | Partially | 10 permanent residents, two companies, middleman/buyer/shop, two final deliveries, mechanic's debt, extortion and appeals. | Wars OCG for districts/enterprises, endless story generator, large criminal economy and player prison. [P2]; S060; E:tools/crime_district_20261016/test_report.json |
| SYS-55 Urban work and delivery | Tested in selected scenarios | Real parcels between NPCs, unique cargo, deferred unit payment, refusal when the recipient is dead, repair orders. | Expansion of professions/employers/territories and all branches of order disruption; these are not 100 completed professions. [P2]; S324; E:tools/city_systems_20261019/validation_final.json |
| SYS-56 Reputation | Partially | Witness/area/organization, propagation delays, impact of work/debt, application trading prices 0.85–1.15. | Shared relationship economics, all Anomaly merchants, autonomous social consequences, and big world enmity/politics. [P2]; S324; CODE:cczmp_city_model.script |
| SYS-57 Local Infrastructure | Tested in selected scenarios | 3 design/power/communication nodes, 100 m radius, device network shutdown, real materials/tools/repair order. | Complete electrical circuit diagram of the map, control of all lamps, generation/loads of plants and physical panels. [P2]; S324; E:tools/city_systems_20261019/validation_final.json |

### Economy

| System | Status | What already exists | What's left/foundation |
|---|---|---|---|
| SYS-58 NBZ: personal accounts and transfers | Partially | Cash is separated from balance, NPC accounts, transfers, deposits/loans, locks, owner session and journal. | Double entry ledger, company/treasury, salaries/budgets and end-to-end audit of all transactions. [P2]; S022; CODE:cczmp_bank.script; S006 |
| SYS-59 Insurance | Code / needed acceptance testing | Catalog and policy/payment API are available; old documents explicitly call the integration incomplete. | Expirations, insurance claims, independent verification of reasons/payments and actual full user flow are not verified. [P2]; S001 Appendix C; CODE:cczmp_bank.script insurance_buy/insurance_payout |
| SYS-60 Companies, Enterprises and Universal Property | technical specification / no implementation found | There are company names/roles and limited transport ownership. | Legal entity, shares, factories/property complexes, transactions/donation/rent/inheritance, rights to land and assets. [P3]; S006 §§9–14; S005 §4 |
| SYS-61 Geology and Terminal Mining | technical specification / no implementation found | Detailed specification of deposits and accounting. | Exploration, ending reserves, licenses, mining equipment, residue conservation and origin of lots. [P3]; S006 §§5–6 |
| SYS-62 Plants, BOMs and Processes | technical specification / no implementation found | There is a target module contract and a small subject workshop. | Complete production orders/machines/capacities/defects/losses, material balance and origin of the finished product. [P3]; S006 §§3–7,19–22 |
| SYS-63 Automotive NChG and own brands | technical specification / no implementation found | NAZ is named as the author; five other titles in technical specification remain working proposals. | Design/drawing, suppliers, certification, series/VIN, sales and actual production of the machine from components. [P3]; S006 §§12–13 |
| SYS-64 Industrial energy, water, heat | technical specification / no implementation found | There are local game service nodes and engineering items. | Generation/networks/power/tariffs, water/sewage/heat and shutdown of production when resources are scarce. [P3]; S006 §8; S324 |
| SYS-65 Warehouses and industrial logistics | technical specification / no implementation found | Parcels, trunks, towing and local deliveries exist. | Lots, reservations, carrying capacity, inter-location shipments, loading equipment and a single cargo balance. [P3]; S006 §11; S324 |
| SYS-66 Market, Taxes and Corporate Finance | technical specification / no implementation found | There are local wallets/prices/personal accounts and separate rules. | Cost/dynamic markets, corporate accounts, taxes, budgets, escrow, bankruptcy and financial reporting. [P3]; S006 §§9–10,16–19 |

### World and content

| System | Status | What already exists | What's left/foundation |
|---|---|---|---|
| SYS-67 Housing and Real Estate | technical specification / no implementation found | ENT, list of property types, logical points of institutions and transport register. | Premises with owner, access/doors/storage, rent, utilities, sale and inheritance. [P3]; S005 §4; S071 S2; S006 §9 |
| SYS-68 Education and 100+ professions | technical specification / no implementation found | Small skills courses, specialists, city orders and service activities. | Universities/colleges/curriculums/exams/diplomas and a large catalog of independent work cycles. [P3]; S005 §§9–10; S019; S324 |
| SYS-69 New maps, buildings and infrastructure | Prototype | Anomaly maps are used; there are world objects and Dam as OGF. | Goldeneye Dam is not a new game location. We need SDK, collisions, navigation, transitions, interiors and routes. [P3]; S005 §12; S370 |
| SYS-70 Story campaign and free life | technical specification / no implementation found | There is an old script/lore and separate local stories with mechanics. | The main campaign, staging, cutscenes and completed story branches from the summary concept have not been confirmed. [P3]; S004; S005 §14; S060 |
| SYS-71 One life and a new identity | technical specification / no implementation found | Deaths and identities of individual NPCs are taken into account; there are basic Anomaly features. | Own cycle of the new CCZMP personality, property inheritance and rules for death from a bug. A full-time Ironman does not prove this cycle. [P3]; S005 §13 |
| SYS-72 Water Transport and Buoyancy | technical specification / no implementation found | Provided by the concept; no confirmed individual working controller found. | One proven hull on the water, buoyancy, entry/exit, damage and retention. [P3]; S005 §3.4; S071 §6 |

### Online

| System | Status | What already exists | What's left/foundation |
|---|---|---|---|
| SYS-73 General server and multiplayer | technical specification / no implementation found | The current offline gaming segment; the site has its own backend and a separate database. | Reputable game server, at least 2 clients, synchronization and recovery; 1000–2000 players is the goal, not capacity. [P3]; S005 §§1.15–16; S001 |
| SYS-74 Server economy, anti-cheat and scaling | technical specification / no implementation found | There are local checks for permissions, logs and some replays. | Network authority, interest management, server transactions, load testing and protection of the common world. [P3]; S005 §§15–18; S006 §§16–18 |

### Website and release

| System | Status | What already exists | What's left/foundation |
|---|---|---|---|
| SYS-75 Website and permanent forum | Partially | Flask backend, frontend modules, SQLite users/categories/boards/topics/posts; registration/login, roles and forum. The database actually exists. | Public deployment/HTTPS, independent acceptance testing security, email/password reset, attachments, avatars, live notifications and complaints. [P2]; S334; CODE:D:/CCZMP PROJECT SITE/backend; SNAPSHOT:database/forum.sqlite3 |
| SYS-76 Local Forum Security | Code / needed acceptance testing | Parameterized SQL, scrypt, CSRF/roles, textContent, query limiting and headers are present in the code. | Legacy JS/CSP unsafe-inline, public configuration and full testing. Do not declare an independent security audit. [P2]; S334; CODE:backend/auth.py; CODE:backend/security.py |
| SYS-77 Licenses and Origin of Resources | Partially | Licenses/sources and CREDITS are saved, there are registries of models/donors. | Checking the rights of specific packages before distribution, including the Batteries package; The presence of license.txt does not in itself mean general readiness. [P2]; S064; S325; S291; license file registry |
| SYS-78 Performance and Graphics Optimization | Partially | There are geometry/texture reports and single game runs of DX9. | LOD, draw calls/polygons/vehicle fleet textures, long-term load, DX10/DX11, memory and collaboration of all systems. [P1]; S056; S298; S370 |
| SYS-79 Team and Invitations | Documents/execution not confirmed | There are tables of candidates and personal texts of invitations. | Submission, consents, roles and actual participation are not proven by these files. No messages were sent to anyone during the audit. [P3]; S308; recruitment tables |
| SYS-80 Ready public assembly | Not confirmed | The development working directory and packages with local checks exist. | Clean installation, reproducible composition, regression, stability, asset permissions, release support instructions and criteria. [P0]; S071; S370; ongoing audit |


## 10. Audit files and navigation

The main report lies at the root `D:\CCZMP PROJECT\docs`. `12_Аудит_проекта_2026-10-28` contains a separate system registry (Markdown/JSON), the current 85 transport sections (Markdown/JSON), parsing of each document (Markdown/JSON), a snapshot of quantities/checks (JSON) and a manifest of the created files. New source documents are collected in `11_Обновления_2026-10-28`; previous sections and historical versions are preserved.

**How ​​to transfer to another developer/AI:** first this report, then `CCZMP_SYSTEMS_REGISTER_2026-10-28.json`, the required thematic document and the code/results of checking exactly its subsystem. Large master concept and economic technical specification are needed as goals; they cannot be presented as a ready-made list.

The detailed origin of each file is in `CCZMP_DOCUMENT_REVIEW_2026-10-28.json`. It has 371 entries with source paths, hash, document role, clauses and output. The review register includes licensed and technical materials; it does not issue each license as a separate concept. The original `CCZMP_items.pdf`/`CCZMP_items_v2_предложения.pdf` were not found in the current passage: their contents are taken into account through the surviving detailed guides, and a direct re-parsing of these missing PDFs is not claimed.

### Primary sources for controversial statuses

| Code | Document | How to use |
|---|---|---|
| S000 | _index__INDEX.md | Historical index of structure and dependency graph; The number of files refers to the generation date, not to 10/28. |
| S001 | CCZMP_technical_guide.md | Snapshot 08.10: restrictions on the bank, investigations, convoy and number of organizations were partially lifted later. Serves as a description of the original rules, not a final status. |
| S004 | CCZMP_merged_cleared.txt | Large mixed lore/scenario/regulations. The old PM indication does not change the factual basis of Anomaly 1.5.1. Names, ranks and desired vehicles do not prove the game systems created. |
| S005 | STALKER_X_CCZMP_MASTER_CONCEPT-1.md | The main long-term vision. Author's ideas, details and suggestions are separated; compared with SYS-01...80, without declaring the concept a finished game. |
| S006 | CCZMP_ECONOMY_INDUSTRY_TECH_SPEC_v1.md | Technical technical specification economics and industry. The proposed eco_* modules, batches, ledger and plants were not found as a complete platform. NAZ is approved in the source; the other five brands are working. |
| S008 | __README_RU.md | Real repositories and documents. The old set of screens was added later; voiceover texts are not the same as actor recordings. The mass/animation of the cover and interlocation acceptance testing remain open. |
| S019 | cczmp_items_tuning_20261010.md | The most comprehensive of the early series subject guides; describes the workshop, medicine, cases and transport. Old statements about the absence of drones/aviation are partially canceled by packages 10/18–22. |
| S022 | ELECTRONICS_SK_GUIDE_RU.md | Separates the virtual network, UID, account and physical owner; confirms the transition from a wallet to a separate balance, automatic checkouts IC. Later 111 and city UI were added. |
| S040 | armor_20261016__README_RU.md | Preparatory mathematical/geometric stand 16.10. The denial of a finished tank refers to this stage; tank and native testing are described later. Air defense/crane capabilities should not be considered done. |
| S042 | CCZMP_—_transport_organizations_by_ranks.pdf | 18-page table of departmental demand and ranks. Contains expressly stated suggestions and assumptions; not a list of machines implemented in gamedata. |
| S045 | README_AIRCRAFT.md | Document of the Mi-2 prototype and landing corrections; it cannot be transferred acceptance testing automatically to the Rafale, Su-27/30 or Ka-52. |
| S048 | TANK_GUIDE_RU.md | Initial tank prototype; further edits to curbs, damage/armor and saves - S330. |
| S054 | VEHICLE_SIGNALS_README_RU.md | General light/signal controller. Lens and damage updates should be read along with the S330; not complete acceptance testing of the entire park in all renders. |
| S056 | vehicles_work__README.md | W140 with the most specific single runtime checks; high geometric cost, no complete door kit/LOD. |
| S059 | CIVIC.md | Departmental pilot in Rostock; individual procedures have been verified. An open containment facility is not a physical prison. |
| S060 | CRIME_DISTRICT_GUIDE_RU.md | First crime district with 10 residents, ultimate quests, real money/stuff and individual relationships. Not autonomous economy/war of all OCG. |
| S061 | DOCUMENTS.md | Subject documents and input corrections are confirmed; The presentation film animation does not follow from the presence of the UI. |
| S064 | STATE_UNIFORMS.md | Chevrons and native ranks were tested on 19 NPCs. The 13 government organizations in this package are not equal to the number of the entire current register; The license for the Batteries package remains an issue. |
| S066 | README_radio_air.md | The later general radio airplay and position retention replaces the earlier track restart scenario. The described lack of flight transport refers to stage 10.10. |
| S071 | CCZMP_STABILIZATION_PLAN.md | Stabilization and vertical cut plan: S0/S1 have been partially accepted, S2 has received deliveries/repairs/investigations, but the rental of the premises and the entire end-to-end cycle have not yet been confirmed. |
| S074 | README_STABILIZATION.md | Implemented limited life pilot of three employees; needs are not equal to food consumption or the autonomous life of the population. |
| S075 | stabilization_work_20261012__TEST_REPORT.md | Native report on UI/three NPCs with time consumption correction on loading. Do not accept test numbers as the current full set. |
| S324 | CCZMP_CITY_SYSTEMS_2026-10-19.md | Current urban subsystems and their limitations. Late native_loaded_verification additionally confirms the restoration of part of the shipment after cold loading. |
| S325 | CCZMP_DONOR_COMPLETION_2026-10-18.md | Closes the old eight untransferred vehicles and inventory-only drones: 203–210 and fa_042–045 have appeared. FPV/unique special mechanisms are still not ready. |
| S326 | CCZMP_GADGETS_111_2026-10-19.md | UI, ZonaTaxi and 111; open checks do not all remain open: the procedure/transportation is clarified by S324 and later journals. General acceptance testing 111 not completed. |
| S328 | CCZMP_TRANSPORT_STATUS_2026-10-17.md | Registry 10/17 historical: 46 sections, eight missing vehicles and drone items. These numbers/statuses are replaced by subsequent resources. |
| S329 | CCZMP_TRANSPORT_STATUS_2026-10-18.md | Register 10/18: 58 sections. In the table of drones, the subject section is indicated in places, and the physical flying section is given separately - do not count as doubling the transport. |
| S330 | CCZMP_VEHICLE_FIX_2026-10-18.md | Specific native tests of the tank/W140 and light/damage adjustments. They are not road tests for all vehicles. |
| S334 | docs__README.md | A real standalone Flask/SQLite site, not just monolithic HTML. Local functionality and publishing/independent security have different statuses. |
| S340 | AUDIT.md | Inventory 238 ZIP as of 10/23. The classification by path is preliminary and does not confirm the operation of the models. |
| S342 | LATEST_INTEGRATION_WORKLIST.md | Acceptance queue from 10/23 is not an up-to-date list of missing OGFs: 25 new sections are already in gamedata. Unique mechanism/test requirements remain relevant. |
| S370 | STATUS_RU.md | Main package status 10/22. The log after writing the document further confirms the cold recovery of the two machines; The original warm access violation is not declared resolved. |

**Report boundary:** status of available documents, installed files and saved results as of 10/28/2026. Does not confirm public release, full balance, independent security audit, rights to all assets, or operation of untested game branches.
