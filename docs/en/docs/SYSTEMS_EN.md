[Русский](../../SYSTEMS_RU.md) · **English** · [Documentation index](INDEX.md) · [Translation notes](../TRANSLATION.md)

# CCZMP - current registry of 80 development areas

Update: 10/29/2026. Basic lines - audit 28.10; clarifications below take into account Autonomous Life V1 and the public Locks module. This is not a repeat of in-game acceptance testing.

[Status](STATUS_EN.md) · [Index](INDEX.md) · [Change history](CHANGES_EN.md)

The designations `Snnn`, `CODE:` and `E:` are inherited from the original audit and refer to the internal body/working assembly paths; they do not mean that these files are available on public GitHub. Public reasons for clarification: [Life V1](snapshot-2026-10-28/13_Autonomous_Life_V1/README.md), [Locks](../modules/cczmp-locks/README.md), [original audit](snapshot-2026-10-28/CCZMP_PROJECT_FULL_REPORT_2026-10-28.md).

"Verified" applies to the scenarios listed, not every combination of conditions. The priorities are the recommendation of this audit and not the author's previously approved plan.

## Base

| ID/system | Status | Already there | Next result | Reason/Priority |
|---|---|---|---|---|
| SYS-01 - Offline build of Anomaly 1.5.1 | Partially | There are working game modules, configs, resources, interfaces and saved native in-game checks. | Total acceptance testing of all current package combinations; clean install and long-term regression. | S001; S071; S074; S075; CODE:gamedata/scripts/cczmp_runtime.script; P0 |
| SYS-02 - Windows, F6/F7, control return | Tested in selected scenarios | Terminal, documents, gadgets, radio, certificates, trunk; transitions and removing your own input capture. | Regression after all new packages, different resolutions, death/deletion of target/change of level. | S061; S075; E:tools/ui_fix_work/verification_result.json; P1 |
| SYS-03 - Persistent Identity and Serialization | Partially | UID of things and persons; ALife storage, ID+name/section checks, pending operations; individual cold loading confirmed. | Combine migrations into a single contract and close the matrix of all subsystems/old saves. Warm crash transport 22.10 and the general transition matrix V1 are not closed; two regular warm-loads after precache protection do not prove overall stability. | S074; S324; S370; E:tools/donor_import_20261022/native_live.log; P0 |
| SYS-04 - Backups and Rollback | Partially | Stages have baseline/installed, protected hashes and rollback with checking other people's changes. | Rebuild the current manifest after visual repair; try installing/rolling back the full release package on a copy. | E:tools/city_systems_20261019/installed.json; E:tools/donor_import_20261022/visual_repair_installed.json; P1 |
| SYS-05 - Indexes and Dependencies | Public indexes updated / local graph requires separate check | Root index, full document directory and FILES.json; the old index 02.10 is archived. | Maintain the generator during changes; The local SQLite graph of the full installation is not rebuilt by this post. | [Reassembly order](INDEXING_EN.md); P2 |

## State

| ID/system | Status | Already there | Next result | Reason/Priority |
|---|---|---|---|---|
| SYS-06 – Organizations and native communities | Partially | 41 organizations in the current factions.ltx; membership, positions, relationships, rights and debug spawn. | 41 records do not mean 41 completed departmental cycles, bases and vehicle fleets. Check all ranks/issues/connections. | S001; S002; CODE:configs/cczmp/factions/factions.ltx; P1 |
| SYS-07 - Passport, ID, identity register | Tested in selected scenarios | Items and owners, full name/portrait/number, viewing, validity of ID, link to dossier, preservation. | Re-issue of the lost document and calendar aging have not been confirmed; not all departments have a separate complete set. | S061; S001; E:tools/ui_fix_work/verification_result.json; P2 |
| SYS-08 – Animation of presenting documents | technical specification / no implementation found | There are objects, textures and a viewing screen; SVG identity concept IC. | Physically retrieve, open, show and remove a document from a first/third person perspective; similar actions of NPCs. | S062; S063; S005; P3 |
| SYS-09 - Criminal Code, Administrative Code and financial rules | Partially | Texts of regulations and gaming sanctions, powers, fines, debt, terms and orders. | Reconcile clause/rule variances, NPC repetition, property requirements, and full coverage of original proposals. | S001; S002; CODE:configs/cczmp/law; P1 |
| SYS-10 - Investigation → prosecutor's office → court | Tested in selected scenarios | Cases, roles of the author, materials, transfer/return, orders, calculation and confirmation of the decision with the judge. | An autonomous meeting with full procedural roles and assessment of all types of evidence is not ready. | S059; S324; E:tools/gadget_dispatch_20261019/native_procedure_result.json; P1 |
| SYS-11 - Automated Murder Investigation | Partially | Witnesses/visibility, limited identification, team IC on W140, body inspection, physical materials, news. | Drive through complex branches: no road/witnesses, masks, dead crew, several places, level transitions; expand geography. | S022; S324; CODE:cczmp_investigations.script; P1 |
| SYS-12 - Evidence and Transfer History | Partially | Source, quality, custodian, transmission, weather deterioration of open traces, packaging; independence of witnesses. | Close E2E on contradictions, false indications, all types of physical traces and preservation at every transition. | S324; CODE:cczmp_city_model.script; P1 |
| SYS-13 - Detention, search, seizure, paddy wagon | Tested in selected scenarios | Protocol, separate search warrant, actual transfer of item, re-seizure defense, NPC boarding/delivery. | Restrictions on story NPCs and resistance remain; full player prison and all branches of enforcement are not confirmed. | S324; E:tools/gadget_dispatch_20261019/native_procedure_result.json; E:native_loaded_verification.json; P1 |
| SYS-14 - FSIN and physical prison | Partially | There is a logical point of containment, deadline, retention/release of NPCs; paddy wagon as transportation. | Locked cells, interiors, full facility mode, labor/regime and physical confinement of the player. | S001; S059; S324; P3 |
| SYS-15 - Appeal and Reversal | technical specification / no implementation found | Justification and cancellation of active orders exist in their own threads. | A complete review of the entered decision, return of the collected fine and cancellation of all property/service consequences. | S001; S002; P2 |
| SYS-16 - Departmental Bases and Maintenance | Partially | Rostock site pilot, base/employees IC to Dead City, job roles and calls. | Separate verified databases of all institutions, interiors, premises and maps according to a large concept. | S059; S022; S005; CODE:cczmp_deadcity.script; P3 |

## Communication and gadgets

| ID/system | Status | Already there | Next result | Reason/Priority |
|---|---|---|---|---|
| SYS-17 - Physical Devices with UID | Tested in selected scenarios | Charge, OS, SIM/tariffs, locks, memory, programs, files, contacts, settings and sessions belong to the subject. | A separate complete visual model of each brand, resource limitations of all combinations and long-term scenarios. | S019; S022; S326; E:city_native_result.json; P2 |
| SYS-18 - Application Interfaces and Stores | Partially | Native CUI, official store, F-zondroid, compatibility, memory, purchase and installation; 51 catalog entries. | 51 entries does not equal 51 independent, fully verified applications; professional programs use a common layout. | S022; S326; CODE:cczmp_app_catalog.script; CODE:cczmp_app_views.script; P2 |
| SYS-19 - Messages, calls, contacts | Partially | In-game address communication, history, text questions/answers, tariffs; correspondence restored after loading. | Full audio calling, voice multiplayer, and random conversational AI have not been confirmed. | S022; S326; E:native_loaded_verification.json; P2 |
| SYS-20 - Public services and personal profile | Partially | Citizen account, documents, position, affairs, debts, search, personal transport. Missing taxes are not made up. | Full tax/social accounting, unified corporate register and all government services of a large concept. | S326; S324; CODE:cczmp_gov_profile.script; P2 |
| SYS-21 - Remote device protection | Tested in selected scenarios | Lost/banned, session revocation, PIN/one-time recovery, history and botnet connection. | Extended regression of owner rights, loss of control equipment, offline objects and old saves. | S324; E:tools/gadget_dispatch_20261019/city_native_result.json; P2 |
| SYS-22 - In-Game Networking and Hacking | Partially | Virtual services .nchg, scanning, protection/ports, tasks, files, decryption, botnet, interference, audit of operations. | Content/balance expansion and native regression of all tools. These are game simulations, not a full-fledged OS/external network. | S019; S022; CODE:cczmp_electronics.script; CODE:cczmp_hacking.script; P2 |
| SYS-23 – Radio “Voice of Pripyat” | Tested in selected scenarios | General broadcast by seconds inside saving, music/inserts, radio of the world/car/PDA, saving switching on and position. | Content of special stations, quality and rights to recordings; independent bypass of maps and DX modes; There is no network synchronization. | S066; S067; E:tools/radio_air_work_20261010/installed_audit.json; P2 |
| SYS-24 - Voice acting for organizations | Partially | There are texts and cue connection points, radio inserts and service signals. | Full voice acting of dialogues and ready-made unique replicas of all organizations have not been confirmed; playback scripts and acting recordings. | S008; S066; CODE:cczmp_voice.script; P3 |

## Items and engineering

| ID/system | Status | Already there | Next result | Reason/Priority |
|---|---|---|---|---|
| SYS-25 - Item Catalog and Trade | Partially | 197 entries in the main items catalogue, real items/supplies, tools, materials, medicines, equipment and donor items separately. | Full compliance with all source PDFs and unique visual models; prices and assortment require balancing. | S019; CODE:configs/cczmp/items.ltx; P2 |
| SYS-26 - Workshop, skills, recipes | Tested in selected scenarios | Time, tools, material consumption, experience/approvals; repair, assembly of devices and kits. | Physical workplaces and full-fledged technological processes of factories; end-to-end material accounting. | S019; S024; S035; CODE:cczmp_engineering.script; P2 |
| SYS-27 - Measuring instruments and instrumentation | Partially | Devices as objects/conditions of operations; gaming diagnostic actions. | Physical measurements of real circuits, oscilloscope waveforms, calibration, benches and deep automation. | S019; S005; S006; P3 |
| SYS-28 — Cases, combination locks and master keys | Tested in selected scenarios / published test harness | PIN, limits, locks, initial items and pending transfers, saved opening operation; The code for stage 09.10 and a stand with 21/21 mock tests have been published, repeat 29.10. | Doors and locks of physical buildings, full subject animation; native regression after all subsequent packages. | [Sources](../modules/cczmp-locks/README.md); [protocol](../modules/cczmp-locks/TEST_REPORT.md); P2 |
| SYS-29 - Artifact Container | Tested in selected scenarios | Transfer of real two artifacts to a hidden container, weight and condition, sales bonus. | Physical cooling/nutrition; additional native checking of map transitions. | S019; S072; P2 |

## Medicine and weapons

| ID/system | Status | Already there | Next result | Reason/Priority |
|---|---|---|---|---|
| SYS-30 - Diseases and Medical Actions | Partially | Game disease states, recipes/dosages, tourniquet/gangrene, specialized specialists, defibrillator for live critical NPC. | Balance and all disease/treatment combinations; graphics and full hospital/operations of a large concept. | S019; CODE:cczmp_medicine.script; P2 |
| SYS-31 - Licenses and Recipes | Tested in selected scenarios | Physical form + owner + admission record, categories A/B/C/D, certificate IC, recipe and limitation of use. | Remaining legal scenarios, re-release and full coverage of original legal proposals. | S008; S019; CODE:cczmp_licenses.script; P2 |
| SYS-32 - Ammunition, armor, shield, special equipment | Partially | Real packs, ammo options, head/body protection, wear, heavy equipment restrictions, gas/taser. | Author's animations of the shield/hands, visual refinement of sets and balance of all combat combinations. | S019; CODE:cczmp_gear.script; P2 |
| SYS-33 - Donor Weapon | Partially | 7 weapon entries from the donor catalog; game databases and HUD/world models, including Operator and Vandal. | Check each set/option and state transitions separately; own animations and accuracy of real performance characteristics have not been confirmed. | S325; CODE:configs/cczmp/donor_catalog.ltx; P2 |

## Characters

| ID/system | Status | Already there | Next result | Reason/Priority |
|---|---|---|---|---|
| SYS-34 - Forms and Models of Organizations | Partially | 7 native/state options, special forces rank package; 6 donor NPC records, including SChS. There are game promotion/demotion checks. | Unique, accurate uniform/equipment for each department and rank; rights to distribute individual packages. | S064; S298; S325; E:state_uniforms_20261009/verification_result.json; P2 |

## Transport

| ID/system | Status | Already there | Next result | Reason/Priority |
|---|---|---|---|---|
| SYS-35 - Basic Automotive System | Tested in selected scenarios | CCar, engine/fuel/damage, purchase/rent/issuance, GPS, blocking, physics and saving individual cars. | Individual finishing and complete acceptance testing of each body, interior, entry/exit; LOD and large vehicle fleet. | S019; S056; S330; CODE:cczmp_transport.script; P1 |
| SYS-36 - New Models October 22 | Prototype | 25 OGF: 23 transport sections and 2 world objects; file/sections/materials are present, 25 sections are recognized in the test. | driving tests all machines; for bus/airplane there is no_place; 2 cars were restored cold, the warm crash was not explained. | S370; S342; E:tools/donor_import_20261022/native_live.log; P0 |
| SYS-37 – Tank NChG | Tested in selected scenarios | Physical rollers/drive, turret/ammo, HE/AP, damage/armor, curb and cold loading in tests. | Finalization of the hull/chassis/controls, a full fleet of heavy vehicles, all renderings and a long stress test. | S048; S330; E:tools/vehicle_fix_20261017/final_verification.json; P1 |
| SYS-38 - Mi-2 and new manned aircraft | Prototype | Mi-2 with holder/flight; Rafale, flying motorcycle, Ka-52, Su-30/Su-27 models use a common base with settings. | Aircraft aerodynamics, own controllers/cockpits, Ka-52 rotors, proven flight of new models. | S045; S370; CODE:cczmp_aircraft.script; P2 |
| SYS-39 - Remote DJI/Shahed | Partially | 4 physical devices, launch from an object, control from the ground, charge/communication/reconnaissance, collection/destruction, saved native data. | FPV video channel and device camera; unique aerodynamics/animations, extended acceptance testing of all profiles. | S325; E:tools/donor_completion_20261018/native_drones_final.json; P2 |
| SYS-40 - Trains and Subways | Prototype | EMD GP7, Alstom Metropolis, InterCity 125 have been moved to physical automotive sections. There is a path/station as objects. | Rail controller, couplers/pointers/signaling, routes and free walking inside moving cars. | S328; S329; S005; S071; P3 |
| SYS-41 - Bus and Passenger System | Prototype | Volvo 7900A as resource/section; Taxi and service transport have their own limited schemes. | Articulation, doors, passenger seats, interior and general NPC passenger CCar; testing of the bus itself has not been completed. | S326; S370; S342; P2 |
| SYS-42 - Cranes, Logging and Air Defense | Prototype | KS-4574/5363, CAT, Tor-M1 and static Liebherr are represented by resources/transport or object. | Lift/load, CAT working parts, radar/SAM Tor; a regular W140 frame does not cover these mechanisms. | S040; S325; S370; P3 |
| SYS-43 - Gustav | Prototype | Stationary installation, stock of shots, direction/range settings, hit simulation. | Real heavy projectile, railway movement, separate installation mechanisms. | S040; CODE:cczmp_emplacement.script; P3 |
| SYS-44 – Ural PES-4320 | Source / non-game resource | There are technical Blender models V04/V07 and preparatory materials. | Game optimization, skeleton/collision/OGF, power generator, interaction and acceptance testing; Ural was not found in the current gamedata. | S046; S052; SNAPSHOT:gamedata/meshes; P3 |
| SYS-45 – Taxi and ZonaTaxi | Partially | Routes/geometry at 23 locations and 69 planned vehicles; payment and physical travel were checked separately; the application books the W140. | Full custom order via app, traffic jams/obstacles and cold loading on all maps; There are no interlocation flights. | S047; S051; S326; E:tools/taxi_world_20261015/verification.json; P1 |
| SYS-46 - Trunk and Real Stuff | Tested in selected scenarios | Two inventories, original items/UID, linked container, no re-transfer, restore from save. | Weight/volume limit, cover, destruction/removal of the machine, full-fledged interlocation acceptance testing of all models. | S008; S066; E:tools/trunk_gadgets_work_20261010/final_verification.json; P1 |
| SYS-47 - Machine Registry and Access | Partially | Owner/agreement/number, key permission, power of attorney, transfer of property, theft/search and access to controls/trunk. | Physical model of the key, all transfers/disputed rights, liens/insurance and a complete unified property register. | S324; CODE:cczmp_city.script; CODE:cczmp_transport.script; P2 |
| SYS-48 - Towing and Recovery | Partially | Spring with damping and opposing forces, coupling/uncoupling; in fact, about 25 m have been covered. There is an order for evacuation/penalty parking. | Full native route to the impound lot and an independent NPC tow truck; acceptance testing all trucks/combinations. | S324; E:tools/gadget_dispatch_20261019/native_towing_result.json; P2 |
| SYS-49 - Lights, sirens, city sound | Partially | Lights/lenses and rear red sources, G horn, organizational sirens, background and clearing sounds when subject leaves. | The entire fleet/all DX, geometric fine-tuning of new bodies, full-fledged flashing lights and unique equipment by department. | S054; S330; CODE:cczmp_vehicle_lights.script; CODE:cczmp_vehicle_audio.script; P2 |

## City and NPCs

| ID/system | Status | Already there | Next result | Reason/Priority |
|---|---|---|---|---|
| SYS-50 - 111 Dispatcher and Crews | Partially | Applications, priority/queue, ambulance/police/OMON/paddy wagon departure, status and history; 4 separate service sections. | The first stage is limited to the Dead City; no guarantee of arrival time, full fight OMON/all departure branches are not closed. | S326; S324; CODE:cczmp_emergency.script; CODE:cczmp_response.script; P1 |
| SYS-51 - Crew and Detainee Transport | Partially | Built-in seated models linked to real ALife NPCs, exit/return and delivery; restoration of part of the transportation is verified. | This is a workaround for the CCar limitation rather than a generic native multi-passenger system; we need to fine-tune all interruptions. | S326; E:tools/gadget_dispatch_20261019/native_loaded_verification.json; P1 |
| SYS-52 - Minimum Life Core 22 Residents | Partially / tested in separate scenarios | UID/ALife, needs, memory, queue, work/vacancies, career, real food and cash transactions; cold loading and return of the same NPCs. Three IC profiles are saved via the adapter. | Similar physical behavior of other citizens, supplies, transition matrix/save-load; full GOAP not accepted. | [Report V1](snapshot-2026-10-28/13_Autonomous_Life_V1/REPORT_EN.md); [tests](snapshot-2026-10-28/13_Autonomous_Life_V1/TEST_REPORT.md); P0 |
| SYS-53 - Complete autonomous life of the population | Partially; full V1 not accepted | Minimum core of 22 existing residents, limited connections/knowledge and group continuity. Career and occupational change tested in a limited organization. | Families, divorces, housing, full GOAP, independent change of organizations, education, elections, criminal deals/wars and the entire population. | [Constraints V1](snapshot-2026-10-28/13_Autonomous_Life_V1/KNOWN_LIMITATIONS.md); P3 |
| SYS-54 - Crime Area | Partially | 10 permanent residents, two companies, middleman/buyer/shop, two final deliveries, mechanic's debt, extortion and appeals. | Wars OCG for districts/enterprises, endless story generator, large criminal economy and player prison. | S060; E:tools/crime_district_20261016/test_report.json; P2 |
| SYS-55 - Urban work and delivery | Tested in selected scenarios | Real parcels between NPCs, unique cargo, deferred unit payment, refusal when the recipient is dead, repair orders. | Expansion of professions/employers/territories and all branches of order disruption; these are not 100 completed professions. | S324; E:tools/city_systems_20261019/validation_final.json; P2 |
| SYS-56 - Reputation | Partially | Witness/area/organization, propagation delays, impact of work/debt, application trading prices 0.85–1.15. | Shared relationship economics, all Anomaly merchants, autonomous social consequences, and big world enmity/politics. | S324; CODE:cczmp_city_model.script; P2 |
| SYS-57 - Local Infrastructure | Tested in selected scenarios | 3 design/power/communication nodes, 100 m radius, device network shutdown, real materials/tools/repair order. | Complete electrical circuit diagram of the map, control of all lamps, generation/loads of plants and physical panels. | S324; E:tools/city_systems_20261019/validation_final.json; P2 |

## Economy

| ID/system | Status | Already there | Next result | Reason/Priority |
|---|---|---|---|---|
| SYS-58 - NBZ: personal accounts and transfers | Partial / V1 integration tested in selected scenarios | Existing accounts, loans/deposits, blocking; move_once adapter and receipts for real salary/food without second balance and re-payment after loading. | Full accounting ledger, companies/taxes/budgets and general regression; an empty treasury leaves an obligation unpaid. | [API V1](snapshot-2026-10-28/13_Autonomous_Life_V1/API_CONTRACTS.md); [tests](snapshot-2026-10-28/13_Autonomous_Life_V1/TEST_REPORT.md); P2 |
| SYS-59 - Insurance | Code / needed acceptance testing | Catalog and policy/payment API are available; old documents explicitly call the integration incomplete. | Expirations, insurance claims, independent verification of reasons/payments and actual full user flow are not verified. | S001 Appendix C; CODE:cczmp_bank.script insurance_buy/insurance_payout; P2 |
| SYS-60 - Companies, Enterprises and Universal Property | technical specification / no implementation found | There are company names/roles and limited transport ownership. | Legal entity, shares, factories/property complexes, transactions/donation/rent/inheritance, rights to land and assets. | S006 §§9–14; S005 §4; P3 |
| SYS-61 - Geology and Terminal Mining | technical specification / no implementation found | Detailed specification of deposits and accounting. | Exploration, ending reserves, licenses, mining equipment, residue conservation and origin of lots. | S006 §§5–6; P3 |
| SYS-62 - Plants, BOMs and Processes | technical specification / no implementation found | There is a target module contract and a small subject workshop. | Complete production orders/machines/capacities/defects/losses, material balance and origin of the finished product. | S006 §§3–7,19–22; P3 |
| SYS-63 - Automotive industry NChG and own brands | technical specification / no implementation found | NAZ is named as the author; five other titles in technical specification remain working proposals. | Design/drawing, suppliers, certification, series/VIN, sales and actual production of the machine from components. | S006 §§12–13; P3 |
| SYS-64 - Industrial energy, water, heat | technical specification / no implementation found | There are local game service nodes and engineering items. | Generation/networks/power/tariffs, water/sewage/heat and shutdown of production when resources are scarce. | S006 §8; S324; P3 |
| SYS-65 – Warehouses and industrial logistics | technical specification / no implementation found | Parcels, trunks, towing and local deliveries exist. | Lots, reservations, carrying capacity, inter-location shipments, loading equipment and a single cargo balance. | S006 §11; S324; P3 |
| SYS-66 - Market, Tax and Corporate Finance | technical specification / no implementation found | There are local wallets/prices/personal accounts and separate rules. | Cost/dynamic markets, corporate accounts, taxes, budgets, escrow, bankruptcy and financial reporting. | S006 §§9–10,16–19; P3 |

## World and content

| ID/system | Status | Already there | Next result | Reason/Priority |
|---|---|---|---|---|
| SYS-67 - Housing and Real Estate | technical specification / no implementation found | ENT, list of property types, logical points of institutions and transport register. | Premises with owner, access/doors/storage, rent, utilities, sale and inheritance. | S005 §4; S071 S2; S006 §9; P3 |
| SYS-68 - Education and 100+ Professions | technical specification / no implementation found | Small skills courses, specialists, city orders and service activities. | Universities/colleges/curriculums/exams/diplomas and a large catalog of independent work cycles. | S005 §§9–10; S019; S324; P3 |
| SYS-69 - New maps, buildings and infrastructure | Prototype | Anomaly maps are used; there are world objects and Dam as OGF. | Goldeneye Dam is not a new game location. We need SDK, collisions, navigation, transitions, interiors and routes. | S005 §12; S370; P3 |
| SYS-70 - Story campaign and free life | technical specification / no implementation found | There is an old script/lore and separate local stories with mechanics. | The main campaign, staging, cutscenes and completed story branches from the summary concept have not been confirmed. | S004; S005 §14; S060; P3 |
| SYS-71 - One Life and a New Identity | technical specification / no implementation found | Deaths and identities of individual NPCs are taken into account; there are basic Anomaly features. | Own cycle of the new CCZMP personality, property inheritance and rules for death from a bug. A full-time Ironman does not prove this cycle. | S005 §13; P3 |
| SYS-72 - Water Transport and Buoyancy | technical specification / no implementation found | Provided by the concept; no confirmed individual working controller found. | One proven hull on the water, buoyancy, entry/exit, damage and retention. | S005 §3.4; S071 §6; P3 |

## Online

| ID/system | Status | Already there | Next result | Reason/Priority |
|---|---|---|---|---|
| SYS-73 - General server and multiplayer | technical specification / no implementation found | The current offline gaming segment; the site has its own backend and a separate database. | Reputable game server, at least 2 clients, synchronization and recovery; 1000–2000 players is the goal, not capacity. | S005 §§1.15–16; S001; P3 |
| SYS-74 - Server economy, anti-cheat and scaling | technical specification / no implementation found | There are local checks for permissions, logs and some replays. | Network authority, interest management, server transactions, load testing and protection of the common world. | S005 §§15–18; S006 §§16–18; P3 |

## Website and release

| ID/system | Status | Already there | Next result | Reason/Priority |
|---|---|---|---|---|
| SYS-75 - Website and permanent forum | Partially | Flask backend, frontend modules, SQLite users/categories/boards/topics/posts; registration/login, roles and forum. The database actually exists. | Public deployment/HTTPS, independent acceptance testing security, email/password reset, attachments, avatars, live notifications and complaints. | S334; CODE:D:/CCZMP PROJECT SITE/backend; SNAPSHOT:database/forum.sqlite3; P2 |
| SYS-76 - Local Forum Security | Code / needed acceptance testing | Parameterized SQL, scrypt, CSRF/roles, textContent, query limiting and headers are present in the code. | Legacy JS/CSP unsafe-inline, public configuration and full testing. Do not declare an independent security audit. | S334; CODE:backend/auth.py; CODE:backend/security.py; P2 |
| SYS-77 - Licenses and Origin of Resources | Partially | Licenses/sources and CREDITS are saved, there are registries of models/donors. | Checking the rights of specific packages before distribution, including the Batteries package; The presence of license.txt does not in itself mean general readiness. | S064; S325; S291; registry of license files; P2 |
| SYS-78 - Performance and Graphics Optimization | Partially | There are geometry/texture reports and single game runs of DX9. | LOD, draw calls/polygons/vehicle fleet textures, long-term load, DX10/DX11, memory and collaboration of all systems. | S056; S298; S370; P1 |
| SYS-79 - Team and Invitations | Documents/execution not confirmed | There are tables of candidates and personal texts of invitations. | Submission, consents, roles and actual participation are not proven by these files. No messages were sent to anyone during the audit. | S308; recruitment tables; P3 |
| SYS-80 - Ready public build | Not confirmed | The development working directory and packages with local checks exist. | Clean installation, reproducible composition, regression, stability, asset permissions, release support instructions and criteria. | S071; S370; ongoing audit; P0 |
