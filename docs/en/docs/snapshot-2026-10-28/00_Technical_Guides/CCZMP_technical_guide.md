[Русский](../../../../snapshot-2026-10-28/00_%D0%A2%D0%B5%D1%85%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5_%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%B0/CCZMP_technical_guide.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# CCZMP: help on installed systems

Status as of October 8, 2026. The basis is the installed offline build of Anomaly 1.5.1 in `D:\CCZMP PROJECT`, its active Lua scripts, LTX configs, Russian localization and saved results of game checks. The name of the project contains MultiPlayer, but a network server and cooperative play are not implemented by these modules.

The reference covers bank, organizations and relationships, laws, powers, cases and evidence, detention and escort, departmental area, documents, services and infrastructure, W140 and debugging. Descriptions from technical specification and catalogs are separately marked: the presence of a line in the config does not always mean complete game mechanics.

## 1. Logging in and debugging

- **F6** opens the CCZMP terminal: wallet and bank rating, deposits, loans, organizations, legal status, powers and departments in the world.
- **F7** opens the standard debugger when Debug mode is enabled in the launcher. It adds entry to CCZMP organizations. You can change the organization, create its representative and choose your position.
- Position in the interface is numbered starting from 1; internal `rank` starts from 0. For example, the seventh stage MVD has `rank=6`.
- For actions through own powers, the target is selected at gunpoint before opening the window or from the list of NPCs within 15 m. Most direct actions require a distance of up to 4 m from the performer to the target. When contacting an employee, the performer is that employee.
- The introduction changes the real community of the player in the engine, and not just the inscription. It affects NPC relationships. When changing organizations, the position is reset to the first level. Exiting through the interface restores the original community.
- The debugging position gives authority, but does not cancel warrants, requirements for evidence, stage of the case, distance and permissible target.

| What to create | Menu/ID | What happens |
|---|---|---|
| W140 | F7 → Object spawner → Vehicles; `cczmp_veh_w140` | A real physical car. Spawn on a free flat area |
| Passport | F7 → Item spawner → Items (Note); `cczmp_passport` | Subject of the document, but the normal spawner does not assign an owner |
| ID | Ibid; `cczmp_service_id` | An item without an automatically created connection with a person |
| Representative of the organization | F7 → CCZMP → organization → create representative | An ordinary NPC of your community; section `sim_cczmp_<id>` |
| Building, camera, electrical network | There is no special CCZMP spawner | "Construction" now registers a logical node rather than creating a building |

For documents, standard automatic delivery is recommended. It creates and connects an object with a person. If a document has already been issued and was lost, there is no automatic reissue. A normal debug respawn creates an instance for which the view item may be present, but the window will not open: the owner record is missing. Internal `cczmp_documents.ensure_documents(npc)` is also not a reissue - it takes into account the mark of the previous issue.

## 2. Passport and service ID

Live online characters, including the player, are gradually receiving the passport. The certificate is issued if you belong to a law enforcement organization: police, MVD, FSIN, SChS, IC, OMON, Vympel, Alpha, army. The court and prosecutor's office are not on the current list of issuing security certificates.

The output is checked once per second and processes up to two records per update; If there are a large number of NPCs, a slight delay may occur. The owner is issued one copy of each suitable type. A new game creates a new registry; in the old save game, personalities are created as characters appear online.

The document contains a permanent first name, last name, age 18–65 years, a six-digit number and a profile portrait. With one call sign, the first and last names are assigned once, the call sign is stored separately. For a name with a military prefix, the rank is separated from the personal name. Age is assigned, but there is no separate calendar for growing up now.

The ID shows the CCZMP organization and position, not Anomaly's combat rating. Upon leaving the security organization, the previously issued certificate becomes invalid. Data is updated when an available owner is contacted; The saved entry is shown to the owner offline.

Access:

- In a normal conversation, a security officer may ask for the interlocutor’s passport.
- You can ask for a security officer’s service ID regardless of your organization.
- During a service check, switching between passport/valid ID is available, if it exists for the owner.
- An item in the inventory is opened through “View Document”; closes with the button or Esc.
- “Check against the official register” is available if you have permission to read the dossier. The register shows cases, warrants and detentions of the document owner.

Transfer or theft does not change ownership. Another NPC's passport does not become yours and does not grant membership or powers. Masking by clothing does not replace a real organization for verifying the right to demand documents.

The passport weighs **0.08 kg**, the ID **0.06 kg**. The cost of both is **0**, regular trading is disabled, items are not marked as quest items. Added individual models, textures, icons and viewing with a character portrait. Document dialogues are included in 1816 profiles; If the engine prohibits a character from talking, this is not possible.

## 3. Cases: what is evidence

The case contains the target's permanent identity, article, stage, materials and action history. The author of each action is recorded along with the organization and position at that moment. Changing your organization does not destroy your business.

Basic sequence: **investigation → referral to prosecutor → confirmation by prosecutor's office → judicial review → warrants and/or decision**. A refund sends the case back for revision. You cannot duplicate an open case against the same person under the same article.

To transfer the case and warrant, the presence of material is sufficient; There is a stricter test for sentencing: there must be material that **is not a statement and whose article exactly matches the article in the case**. This is a technical examination of structured records, not a semantic analysis of free text.

| Material | How does | Sufficient for a conviction? |
|---|---|---|
| Statement | Entering text by an authorized person | No. Basis for working with the case |
| Civil Complaint | Action "complaint" | No; observation specifically excludes complaints |
| Interrogation text | Interrogation of a held target | By itself, no; entry does not receive article |
| Search inventory | Real NPC Inventory by Separate Court Order | By itself, no; the presence of things does not automatically qualify |
| Weapons in hands | “Observation” in the case of Criminal Code 3.3, the target is close, the active object is a weapon and it has not been removed | Yes, according to Criminal Code 3.3 |
| Reported kidnapping/ransom | Module actions, event Criminal Code 3.1 | Yes, after adding observation to the case under the same article |
| Offering/receiving a bribe | “Bribery” action, Criminal Code 4.1/4.2 | Yes after adding the corresponding event to the case |
| Node sabotage | Action "sabotage", Criminal Code 2.2 | Technically yes according to Criminal Code 2.2; there is a discrepancy with the description of the article, see below |
| Robbery, artifact theft, PDA hacking, escape, sound pulse | Registered module actions without assigned article | By themselves, no: the article field is empty |
| A common shootout or murder in the world | Regular combat event | There is no automatic material and condemnation on these events now |

The Observe action brings relevant events to the case and/or captures the weapon. You cannot add the same source of the same type again. Free text like "he killed a man" does not create a verified murder event.

Qualification restrictions:

- Criminal Code 3.3 in the text of the law - “Carrying weapons openly is regarded as terrorism.” The check is now looking at the weapon in active hands and the fact that it has not been stowed. It does not analyze license, authorized area, self-defense, or law enforcement exception.
- Sabotage of an infrastructure node is recorded as Criminal Code 2.2, although the description of Criminal Code 2.2 is “Damage of state. transport". This is an existing mismatch between implementation and description; A separate qualification for sabotage is needed in the future.
- `hook` in LTX articles - description of the proposed integration. The presence of `npc_death`, `trade` or another `hook` does not mean that automatic crime registration is working.
- A document, screenshot or item cannot be arbitrarily attached as a new type of evidence. A passport serves as identification, not proof of guilt.

Working example: select an ordinary NPC with a weapon in his hands → case Criminal Code 3.3 → record surveillance from a distance of up to 4 m → transfer to the prosecutor → confirm for the court → obtain the necessary warrants → execute an arrest → pass a sentence → transfer FSIN. The example confirms the current simplified test; it does not model a full assessment of the legality of carrying a weapon.

## 4. Court, warrants, terms and retention

| Authority | Minimum level in the interface |
|---|---|
| IC: open a case | 2 |
| IC: hand over to the prosecutor / arrest | 3 |
| MVD: arrest | 7 - Corporal |
| MVD: transfer to the prosecutor | 10 |
| Court: administrative orders/decision | 8 – Justice of the Peace |
| Court: Criminal Warrants/Judgment | 9 - District Judge |
| Court: protected officials | 15 - Supreme Judge |
| Barricade: Robbery/Kidnapping | 9 |

Other organizations have their own list of powers. Where there is no rank table in technical specification, a numerical career ladder is not invented.

Arrest and search require **different warrants**. The order is active until executed or canceled; after execution, the one-time sanction becomes `executed`. The search reads the actual contents of the inventory and creates an inventory, but does not automatically confiscate all items found. The warrant is canceled by a judge of sufficient position; You cannot cancel an already executed order through this button.

Immunity in the code is given to judges from level 8 and representatives of government organizations from level 10. For decisions on such persons, a Supreme Judge is needed. Legality and authority are checked again in the backend when the action is performed.

Physical detention/violent logic change is supported for normal living simulation NPCs `sim_*`. Story NPCs and physical detention of the player are excluded by this mechanism. An actively resisting NPC does not submit to detention. When holding, the standard pose/logic is used, the selection of weapons and grenades is prohibited; When released, the stored logic is restored.

Player accompaniment uses the standard companion system. A normal friendly NPC can also be followed without a criminal case. Termination of routine escort is not a universal release button for the arrested person/hostage. Fixed a bug in the standard escort dialogue for NPCs without a simulation squad.

The judge first shows the verdict as a calculation, then confirms it separately. For a fixed sanction, the punishment cannot be changed arbitrarily. For Criminal Code 9.1, lower/middle/upper limits of 1/3/5 years are available. The old sentence action in F6 applies the lower bound.

**Term scale:** one legal year is now equal to one in-game day; the maximum of this period is 10 game days. Criminal Code 3.3 with five years gives 5 in-game days, or 432,000 in-game seconds. Brief arrests are set by the game clock, a maximum of 24 hours. These are not real hours on a computer. Variables `real_seconds_per_game_day` in old config comments are not used to recalculate current banking and court deadlines. In fact, the game time `CTime` is applied; sleep and calendar acceleration shift deadlines.

Preliminary arrest of NPCs ends after 24 game hours in the absence of a conviction. After the verdict, the term of imprisonment starts **when FSIN is placed in a detention center**, and not from the opening of the case. If the convicted person has not yet been accepted FSIN, the countdown of the prison term has not yet begun. Automatic release is checked for available online NPC; offline release/recovery may complete when it comes back online.

FSIN can register a prison clause in the executor's position. To receive, you need a convicted prisoner, term >0, a point on the current map, a performer within 5 m from the point and a target within the limits of permissible interaction. The content now represents a logical point and NPC hold rather than a ready-made lockable chamber.

The NPC's fine is deducted from his real money; what is missing is recorded as a debt. Sanctions may include dismissal, suspension, emergency, license revocation, reprimand or demotion. This does not mean creating new license subjects and a complete administrative procedure. The player's sentence fixes the terms/sanctions in a legal state, but there is no physical prison for the player.

Acquittal closes the case, cancels active warrants on it, and releases the held target. A full appeal is disabled in the powers: the return of a previously collected fine and the cancellation of all consequences have not yet been implemented. Repetition in the old player sanctions module and direct NPC sanctions are different: NPCs do not yet have automatic doubling of punishment for repetition enabled. FP 4's property claims for amounts are not available in the normal flow of cases.

## 5. Office area in Rostock

At `l05_bar`, in the courtyard near the fire, around X=200, Z=110, five employees are created: investigator IC, prosecutor, District Judge, patrolman MVD and inspector FSIN. Initialization occurs when the player approaches the site area. They are available through the usual response “Contact a service issue”; F6 also shows list and distances. The judge marks the area on the map.

Employees are created one per role and are not duplicated under loading. There is no automatic revival of the dead. These are ordinary vulnerable NPCs with standard models. Player hostility and combat can block the reception; reputation is not specifically reset.

The investigator, prosecutor and judge act on the player's requests. There are no automatic mass investigations/convictions. The patrol independently executes existing active warrants: searches for a common target within 35 m from itself and 50 m from the base, approaches and detains if there is no resistance. The player and site employees have been excluded from the search.

After the arrest, the detainee goes to point FSIN along the AI ​​grid, a patrol accompanies him. In the event of a battle, the disappearance of an escort, a strong gap in the distance or a timeout, the convoy returns to normal holding. Moving to another map is not a continuous convoy journey: the state is saved, execution is suspended. There is no separate transport for transporting prisoners.

The court and IC in Pripyat, independent departmental bases, special interiors, cells and a new uniform have not yet been built. An ordinary representative of an organization created through the debugger does not automatically become an employee of this site with its reception and route.

## 6. Organizations, services and infrastructure

**34 separate organizations** are registered with their own native communities and NPC/player connections. They differ in the engine, not just in the reference book. The purpose, transport, equipment, location and tasks from the technical specification cards are not equal to the automatically created bases, vehicle fleets and quests.

CCZMP relations range from −100 to 100: alliance from +40, enmity from −40. For the engine, the value is scaled ×50; A friendly relationship is established between the same organization. The relationship is symmetrical. Anomaly's personal goodwill and relationship history continue to apply. Filling empty Warfare buckets prevents custom communities errors, but does not add a full territorial simulation of all departments.

| System | Real action and costs |
|---|---|
| ZonaStroy: construction | Flow `duct_tape`; node registration in player position: structure 25, power 0, communication 0 |
| Structural Repair | `duct_tape`, +25 to 100 |
| ChernEnergo: power | `batteries_dead`, +25 to 100; need a non-zero construction |
| ComNet: communication | `batteries_dead`, +25 to 100; need food >0 |
| Sabotage | −25 designs, power and communications reset |
| Service station "Kaban": repair | Real weapon or armor of the owner, `sewing_kit_b`, +0.25 condition to 1; car not included |
| Treatment | NPC real health +0.35 to 1; one matching first aid kit `medkit`, `medkit_army` or `medkit_scientic` |
| Radiation removal | One `antirad`, current target radiation is removed |
| Medical Record | Health, radiation, bleeding and name are preserved; does not cure in itself |
| Delivery | The actual selected item is transferred from the player's inventory to the NPC; no automatic reward |
| Research | A real artifact is marked studied once; section, organization, weight and cost are recorded |
| Artifact Theft | The real artifact is transferred from the NPC; source mark and goodwill deterioration by 500 |
| Bribery | Real money goes to the government NPC; goodwill grows to +500 per action, but the arrest/case is not automatically canceled |
| PDA Hacking | The target requires a PDA, the player requires `device_pda_2` or `device_pda_3`; the name, organization and wallet of the target are saved |
| Subber Sonic Pulse | Radius 15 m, hold regular NPCs for 5 game seconds, reload 60 game seconds; requires a battery, it is not consumed now |
| Hitman's contract | The customer has a real live hostile stalker; deposit from the customer’s money up to 5000; payment for killing this target by a player who remains in the killer organization |
| Security/escort | Full-time NPC support plus service recording; there is no separate new tactical AI |

An infrastructure node is searched within 15 m. Its indicators are saved, but do not yet control the lighting of the entire map, radio coverage or visual construction. Research does not automatically create a scientific quest, and PDA hacking does not read full correspondence.

Criminal organizations have robbery, kidnapping, ransom and release of their hostage. Threat requires a weapon in the player's hands or a wounded target; resistance prevents action. The robbery takes the NPC's real available money; the same target is subject to a break of 24 game hours. The ransom is also paid from the NPC's own wallet, and not from the fictitious account of relatives. Barricade additionally prohibits kidnapping allies and requires level nine for robbery/kidnapping.

The Zone of Authority may illegally release an arrested person; Corruption syndicate - bribe; Technobandits - steal and explore artifacts; Barricade, Cobra, Sector0 and Spark - sabotage; Sector0 - hack PDA; Fanatics - explore. Snipers and hitmen are also criminal types and receive general criminal actions. PMC is a contract type.

A catalog of seller discounts exists, but full application to standard trading has not yet been connected. Subbers for government agencies have a data conflict technical specification/config; the function reports an unresolved rule, rather than automatically issuing a confirmed discount. Departmental accounts are still reference accounts, without full management of budgets, transfers and salaries.

## 7. Bank: actual rules

F6 allows you to open/close a deposit and take out/repay a loan. Money is debited/issued from the regular Anomaly wallet. The bank "balance" on the main page now shows the wallet; There is no separate full-fledged account with transfers.

Positive integer amounts are accepted for operations. Contributions are limited to three open entries. The interest is simple, not complex: deposit `floor(сумма × годовая ставка × игровые дни / 365)`, loan `floor(первоначальная сумма × ставка × игровые часы / период ставки)`. The repaid portion of the loan now does not reduce the base for subsequent interest accrual. Interest continues to be calculated until maturity.

Initial rating 100, maximum 200; if the rating is below 40, a new loan is not available. Full repayment adds 5; late/blocking usually removes 25. Late adds a one-time penalty of 15% of the calculated outstanding debt on the term. For products with `on_default`, a bank block is applied, but the actual seizure of vehicles/property and automatic arrest for a loan have not yet been activated.

The blocking prohibits opening and closing deposits, new loans, and purchasing a policy through the API. Repayment of an existing loan is permitted. Time limits are checked by playing time. `until_fixed` requires explicit unlocking; There is currently no automatic correction for documents.

The config contains commissions of 2/1/3/5%, a maximum total debt of 5 million and additional product conditions. Current features do not write off these fees or apply the overall debt limit. `gang_only` and reconciliation are not verified as a complete procedure. A loan with a required guarantor is rejected because the guarantor workflow has not been implemented. The Dark Deal directory therefore does not mean working access only for OCG.

“Legendary Savings” cannot be closed with the usual button: we need the yet unrealized issuance of money by court decision. The deposit “Without the right to withdraw” is not displayed at all by the normal interface. These should not be considered as accessible deposits as the first three.

The insurance catalog and purchase/payment API exist, but there is no separate insurance page in the current F6. The policy is stored by class, with no connection to a specific W140/home and no completed automatic calendar expiration. Destroying a vehicle does not automatically trigger a payout. The current payout function returns `floor(дневной тариф × дни полиса × 0,5)`, not half the value of the car. These functions cannot be considered a complete property insurance system.

Blocking `pursuit`, `ban`, `imprisonment` in the config - consequence tags; by themselves do not trigger a real ban, investigative group or prison. Confiscation there resets the internal bank account `balance`, and not the player's entire regular wallet.

## 8. W140: use and characteristics

Added Mercedes-Benz **600 SEL W140**, section `cczmp_veh_w140`. This is a native `SCRPTCAR`/`CCar` with physics, wheels, landing, engine, gears, light and damage. Regular transport has been retained. Other cars, helicopters and special vehicles from organization cards were not automatically added after the W140.

| Key | Action |
|---|---|
| F | Login/logout; go to the front door and look at the car |
| O | Start/stop engine |
| W/S | Gas forward / braking and reverse according to standard control |
| A/D | Steering wheel |
| Space | Handbrake |
| L | Headlights |

| Parameter | Set value |
|---|---|
| Mass | 2190 kg |
| Model length | 5.213 m |
| Width with mirrors | 2,239 m |
| Drive | Rear wheels |
| Box | Automatic, four forward and reverse gears |
| Main couple | 3.07 |
| Gears 1/2/3/4/R | 3.87 / 2.25 / 1.44 / 1.00 / 3.16 |
| Buck | 100 l; standard when creating full |
| `engine_power` | 408 - game engine parameter, unmeasured power |
| Maximum power/torque revolutions | 5200 / 3800 rpm |
| Idle/Maximum | 650 / 6000 rpm |
| `fuel_consumption` | 6.5 - internal setting; this is NOT 6.5 l/100 km |
| Wheel radius | 0.351 m |
| Headlight range | 35 m |
| `cost` sections | 500,000; this is a config-cost, not implemented car dealership |
| State | Normalized scale 0…1; 1 - integer |
| Geometry | 113,933 triangles, 30 mesh batches, 16 dice |

Fuel consumption in native physics has a dependence on operating time and revolutions. When the fuel runs out, the engine stops. The CCZMP script captures fuel approximately once every 500 ms, before saving and leaving the online object; the entry is bound to the ALife server object. Checked preservation and cold loading with 63.5 l and condition 1.

A separate user process for refilling a canister and repairing a car has not yet been added. CCar has technical fuel methods, but it is not a ready-made service/button in the current CCZMP. The repair shop repairs weapons and armor, not cars. Purchase, ownership, registration numbers, car deposit, passenger convoy and automatically created vehicle fleet are not implemented.

### Damage

| Type of impact | Multiplier from `immunities` |
|---|---:|
| Bullet (`fire_wound`) | 0.06 |
| Explosion | 0.20 |
| Fire | 0.04 |
| Impact/Collision (`strike`) | 0.02 |
| Electricity | 0.001 |
| Wound, radiation, telepathy, chemical burn | 0 |

The multiplier multiplies the incoming impact force rather than removing a fixed percentage of condition per bullet. The bones are set to `hit_scale=1`; wheels and front doors have their own entries `damage_items`: **5000 per wheel**, **3000 per door**. These are the parameters of the local strength of parts in the native damage model, and not the total “5000 HP” reserve of the machine.

Collision coefficients: body root and wheels 0.00001; cab/front doors 0.0001. The explosion config is set to blast radius 5 m, fragmentation radius 20 m, 15 fragments. Damage behavior depends on the type and severity of the hit/collision; separate ballistic tests “how many bullets/grenades” were not carried out. Armor class and guaranteed protection for a seated player are not stated.

Top speed and 0–100 acceleration not measured. You cannot pass off real Mercedes performance characteristics as confirmed in-game ones: the initial X-Ray settings, its power/consumption calculations and physics are used.

Model limitations: no LOD, full door animation is not ready, rear doors are static, engine sound is standard from Niva, dashboard uses static fallback. On large fleets, a heavy model can significantly increase the load. Real test done for one car in Rostock on AnomalyDX9AVX: spawn, entry/exit, start, reverse and forward, turn, handbrake, save/cold loading. Headlights and destruction are not included in the individual interactive runtime checks listed.

## 9. Saving, checks and unfinished parts

The states of the bank, organizations, legal sanctions, cases, orders, liens, services, documents and fuel are stored through ALife storage. Calendar dates use `CTime`. Not only the short-lived object id is checked, but also the saved identity, server object name and section, so that a new NPC does not accidentally inherit the old case.

The latest docs fix unregisters the modal window on close, delays going to the registry until the click is complete, and clears the queue at loading. This restores normal input, inventory and F6/F7. A safe check for a missing squad in the standard conductor/escort dialogue has also been added. Saved results: 128 Lua 5.1 tests and 8 LuaJIT regressions; in real X-Ray, document buttons, registry, Esc, F6/F7, inventory properties, food use and dialogue of an accompanied NPC without a squad were checked. This help is compiled by reading files; a new game session for it did not start.

Based on the results of previous game checks, the scenario case → prosecutor's office → warrant → patrol → convoy → FSIN was passed, and the identity, case, executed warrant, term and five employees were preserved after a cold start. This is a test of a specific pilot scenario, not proof of coverage of all fights, maps and NPCs.

Not completed: network multiplayer; autonomous investigation of any world crimes; player's physical prison; full-fledged buildings and chambers; departmental forms and vehicle fleets; gas station/car service station; registration and purchase of transport; loans with real collateral; insurance of specific property with automatic events; departmental budgets/salaries; full appeal and return of sanctions; automatic execution of all Constitutional and financial norms.

## 10. Where to check and configure

The paths below are for project `D:\CCZMP PROJECT`:

- `gamedata\configs\cczmp\bank\*.ltx`: banking catalog tariffs.
- `gamedata\configs\cczmp\law\*.ltx`: articles, sanctions, scope of terms, Constitution.
- `gamedata\configs\cczmp\factions\*.ltx`: organizations, ranks, relationships and reference accounts.
- `gamedata\configs\cczmp\operations.ltx`: powers, distances, costs and numerical parameters of services.
- `gamedata\configs\cczmp\documents.ltx`: list of organizations issuing certificates and verifying documents.
- `gamedata\configs\models\vehicles\cczmp_w140.ltx`: current physical settings of W140; OGF includes exactly this file.
- `gamedata\configs\items\items\items_cczmp_documents.ltx` and `items_cczmp_vehicles.ltx`: item/machine sections.
- `gamedata\scripts\cczmp_*.script`: actual checks and execution; `tasks_guide.script` - Fixed conversation with NPCs without a squad.
- `DOCUMENTS.md`, `CIVIC.md`, `OPERATIONS.md`: game scenarios and stage boundaries.
- `tools\vehicles_work\runtime_verification.json`, `tools\ui_fix_work`, `tools\civic_work`: saved test results.
- `_index\anomaly.db`, `_index\INDEX.md`: index of resources and symbols for searching dependencies. The index itself is not a game mechanic.

Some old comments in the config describe the plan, not the actual algorithm. For example, the individual banking/court "real time scales" in the comments are at odds with the current use of game time. When configuring, you need to consider which fields the script actually reads.

Next are complete tables from the installed configs and Russian localization.

## Appendix A. Contributions

| Title | Minimum, ₽ | Game days | Rate | Early withdrawal | Condition |
| --- | --- | --- | --- | --- | --- |
| Zone Standard | 50,000 | 30 | 0.7% per annum | Yes; fine 2,000 | Regular output |
| Gray Metal | 100,000 | 90 | 1.4% per annum | Yes; fine 5,000 | Regular output |
| Survival+ | 250,000 | 180 | 2.2% per annum | No | Regular output |
| Legendary savings | 1,000,000 | 365 | 3% per annum | No | Only court; procedure not connected |
| Deposit “No withdrawal rights” | 0 | 36500 | 0.5% per annum | No | Regular withdrawal is prohibited |

With `min=0`, the function still only accepts a positive integer sum. This is a simple annual rate, not a lifetime rate.

## Appendix B. Credits

| Title | Maximum, ₽ | Game days | Rate | Condition fields | Overdue tag |
| --- | --- | --- | --- | --- | --- |
| Initial push | 50,000 | 2 | 1.2% for 1 game hour | Guarantor: 0; agreement: 0; OCG: 0 | none |
| For business | 250,000 | 5 | 0.9% for 1 game hour | Guarantor: 0; agreement: 0; OCG: 0 | none |
| Wheels and shelter | 500,000 | 10 | 0.65% for 1 game hour | Guarantor: 0; agreement: 0; OCG: 0 | transport |
| Prestige | 1,000,000 | 15 | 0.5% for 1 game hour | Guarantor: 1; agreement: 1; OCG: 0 | none |
| Dark Deal | 2,000,000 | 3 | 0.3% for 0.1666667 game hours | Guarantor: 0; agreement: 0; OCG: 1 | none |

All catalog penalties are 15%. "Initial push" is now actually set to 1.2% per game hour, despite the old comment about the 0.9% limit. Dark Deal is set to 0.3% for about 10 in-game minutes (about 1.8% per in-game hour); the comment about real minutes does not correspond to the CTime algorithm. Tags `transport`/`property` are not a ready seizure of property. The guarantor is not realized; product with `requires_guardian=1` is rejected. For other additional conditions, see the main text.

## Appendix C. Insurance catalog (API and data, unfinished game integration)

| Class | Section | 1 day, ₽ | 7 days, ₽ | 30 days, ₽ |
| --- | --- | --- | --- | --- |
| Passenger car (civilian) | ins_car | 15,000 | 90,000 | 250,000 |
| Service transport | ins_official | 25,000 | 150,000 | 450,000 |
| SUVs, jeeps, pickups | ins_offroad | 18,000 | 110,000 | 330,000 |
| Freight transport | ins_truck | 30,000 | 190,000 | 550,000 |
| Air transport | ins_air | 100,000 | 600,000 | 1,800,000 |
| Home | ins_house | 30,000 | 200,000 | 350,000 |
| Dormitory (whole building) | ins_dormitory | 75,000 | 450,000 | 1,300,000 |
| Apartment | ins_apartments | 20,000 | 130,000 | 400,000 |
| Business | ins_business | 100,000 | 600,000 | 1,800,000 |
| Other real estate | ins_other | 50,000 | 300,000 | 950,000 |

Prices - catalog data. The policy is not linked to a specific car/house; automatic insurance event and expiration are not yet enabled.

## Appendix D. Bank blocking

| Rule | Actual period without argument days | Reset internal balance | Consequences tag | Pursuit tag |
| --- | --- | --- | --- | --- |
| br_laundering | Indefinitely | 1 | investigation | schs |
| br_exploit | 30 game days by default | 0 | ban | none |
| br_fake_transfer | 7 game days by default | 0 | freeze_for_investigation | security |
| br_interfer | Indefinitely | 0 | pursuit | schs |
| br_foreign_withdraw | Indefinitely | 0 | imprisonment | schs |
| br_illegal_service | 30 game days by default | 0 | surveillance | none |
| br_credit_fraud | 14 game days by default | 1 | debt_and_arrest | mvd |
| br_mass_transfer | 7 game days by default | 0 | security_check | security |
| br_illegal_funds | 14 game days by default | 1 | confiscation | security |
| br_bad_documents | Before explicit removal | 0 | fix_documents | none |

Tags do not automatically cause world arrest/ban/surveillance. A regular wallet is not reset by the internal balance confiscation flag.

## Appendix E. All 34 Organizations and Their Authorities

| Title | ID | Type | Number of steps | Actions |
| --- | --- | --- | --- | --- |
| ZONASTROY | zonastroy | Enterprise | 5 | Register and equip an infrastructure facility (`build`), Repair an infrastructure facility (`repair_structure`) |
| ChernEnergo | chernenergo | Enterprise | 5 | Restore power to the object (`restore_power`) |
| ComNet NChG | comnet | Enterprise | 5 | Restore object connection (`restore_communications`), Dossier (`dossier`) |
| Court NChG | sud | State | 15 | Dossier (`dossier`), Issue an arrest warrant (`issue_arrest`), Issue a search warrant (`issue_search`), Cancel the warrant (`revoke_warrant`), Convict (lower limit of term) (`convict`), Acquit and release (`acquit`), Return the case for revision (`return_case`), Release the detainee (`release`), Suspend official powers (`suspend`) |
| IC NChG | sk | State | 5 | Dossier (`dossier`), Open a case (`open_case`), Add a statement (`statement`), Record observed facts (`observe`), Search warrant (`search`), Transfer the case to the prosecutor (`submit_case`), Arrest (`arrest`), Record interrogation (`interrogate`) |
| SChS | schs | State | 0 | Dossier (`dossier`), Open a case (`open_case`), Add a statement (`statement`), Record observed facts (`observe`), Search warrant (`search`), Transfer the case to the prosecutor (`submit_case`), Arrest (`arrest`), Record interrogation (`interrogate`), Start convoy/escort (`escort`) |
| Prosecutor's office NChG | prokuratura | State | 0 | Dossier (`dossier`), Open a case (`open_case`), Add a statement (`statement`), Record observed facts (`observe`), Endorse the case for court (`endorse_case`), Return the case for revision (`return_case`), Suspend official powers (`suspend`) |
| Service station "Kaban" | sto_kanban | Neutral | 0 | Repair item (`repair_item`), Transfer item to NPC (`delivery`), Dossier (`dossier`) |
| Subbers | sabbers | Neutral | 0 | Sonic pulse (15 m) (`sonic_pulse`), Give item to NPC (`delivery`) |
| UG "Barricade" | barricade | Criminal | 10 | Rob an NPC (`rob`), Kidnap an NPC (`kidnap`), Receive ransom from NPC funds (`ransom`), Free your hostage (`free_hostage`), Damage an infrastructure facility (`sabotage`) |
| Operators | operators | Neutral | 0 | Transfer item to NPC (`delivery`), Start convoy/escort (`escort`), Complete voluntary escort (`end_escort`) |
| Fanatics | fanatiki | Criminal | 0 | Rob an NPC (`rob`), Kidnap an NPC (`kidnap`), Receive ransom from NPC funds (`ransom`), Free your hostage (`free_hostage`), Explore an artifact (`research`) |
| PMC X-soldiers | pmc | Contract | 0 | Start convoy/escort (`escort`), Complete voluntary escort (`end_escort`), Accept NPC under protection (`guard`) |
| Veteran snipers | snipers | Criminal | 0 | Start a convoy/escort (`escort`), Complete a voluntary escort (`end_escort`), Take an NPC into custody (`guard`), Rob an NPC (`rob`), Kidnap an NPC (`kidnap`), Receive ransom from NPC funds (`ransom`), Free your hostage (`free_hostage`) |
| Clear boys | chetkie | Criminal | 0 | Rob an NPC (`rob`), Kidnap an NPC (`kidnap`), Receive ransom from NPC funds (`ransom`), Free your hostage (`free_hostage`) |
| Stalkers | stalkers | Neutral | 0 | Explore artifact (`research`), Transfer item to NPC (`delivery`), Start convoy/escort (`escort`), Complete voluntary escort (`end_escort`) |
| TO "Punisher" | karateli | Criminal | 0 | Rob an NPC (`rob`), Kidnap an NPC (`kidnap`), Receive ransom from NPC funds (`ransom`), Free your hostage (`free_hostage`) |
| TS “Zone of Power” | zona_vlasti | Criminal | 0 | Rob an NPC (`rob`), Kidnap an NPC (`kidnap`), Receive ransom from NPC funds (`ransom`), Free your hostage (`free_hostage`), Free someone illegally arrested (`prison_break`) |
| Corruption syndicate | korrsyndicat | Criminal | 0 | Rob an NPC (`rob`), Kidnap an NPC (`kidnap`), Receive ransom from NPC funds (`ransom`), Free your hostage (`free_hostage`), Bribe an employee (`bribe`) |
| Technobandits | techno | Criminal | 0 | Rob an NPC (`rob`), Kidnap an NPC (`kidnap`), Receive ransom from NPC funds (`ransom`), Free your hostage (`free_hostage`), Steal an artifact (`steal_artifact`), Explore an artifact (`research`) |
| TO "Black Cobra" | cobra | Criminal | 0 | Rob an NPC (`rob`), Kidnap an NPC (`kidnap`), Receive ransom from NPC funds (`ransom`), Free your hostage (`free_hostage`), Damage an infrastructure facility (`sabotage`) |
| Sector "0" | sector0 | Criminal | 0 | Rob an NPC (`rob`), Kidnap an NPC (`kidnap`), Receive ransom from NPC funds (`ransom`), Free your hostage (`free_hostage`), Hack a PDA (`hack_pda`), Damage an infrastructure facility (`sabotage`) |
| Group "Iskra" | iskra | Criminal | 0 | Rob an NPC (`rob`), Kidnap an NPC (`kidnap`), Receive ransom from NPC funds (`ransom`), Free your hostage (`free_hostage`), Damage an infrastructure facility (`sabotage`) |
| Police | militsia | State | 0 | Dossier (`dossier`), Open a case (`open_case`), Add a statement (`statement`), Record observed facts (`observe`), Arrest (`arrest`), Search warrant (`search`), Record interrogation (`interrogate`), Transfer the case to the prosecutor (`submit_case`), Start convoy / escort (`escort`) |
| MVD | mvd | State | 25 | Dossier (`dossier`), Open a case (`open_case`), Add a statement (`statement`), Record observed facts (`observe`), Arrest (`arrest`), Search warrant (`search`), Record interrogation (`interrogate`), Transfer the case to the prosecutor (`submit_case`), Start convoy / escort (`escort`) |
| FSIN | fsin | State | 0 | Dossier (`dossier`), Arrest (`arrest`), Search warrant (`search`), Start convoy / escort (`escort`), Mark prison point (`prison_site`), Place convict in prison (`admit_prisoner`), Release the detainee (`release`) |
| Scientists | scientists | State | 0 | Research artifact (`research`), Treat NPC (`heal`), Dossier (`dossier`) |
| MChS | mchs | State | 0 | Heal NPC (`heal`), Release Hostage (`rescue`), Repair Infrastructure Facility (`repair_structure`), Start Convoy/Escort (`escort`), Complete Voluntary Escort (`end_escort`) |
| Ministry of Health | minzdrav | State | 0 | Treat NPC (`heal`), Remove Radiation (`decontaminate`), Record Medical Indicators (`medical_record`), Release Hostage (`rescue`) |
| Killers | killers | Criminal | 0 | Take a contract for the customer's enemy (`contract`), Dossier (`dossier`), Rob an NPC (`rob`), Kidnap an NPC (`kidnap`), Receive a ransom from NPC funds (`ransom`), Free your hostage (`free_hostage`) |
| OMON | omon | State | 0 | Dossier (`dossier`), Arrest (`arrest`), Search Warrant (`search`), Start Convoy/Escort (`escort`), Release Hostage (`rescue`) |
| Pennant | vympel | State | 0 | Dossier (`dossier`), Arrest (`arrest`), Search warrant (`search`), Start convoy/escort (`escort`), Release hostage (`rescue`), Take NPC into custody (`guard`) |
| Alpha | alpha | State | 0 | Dossier (`dossier`), Arrest (`arrest`), Search warrant (`search`), Start convoy/escort (`escort`), Release hostage (`rescue`), Take NPC into custody (`guard`) |
| Civil | civilians | Civil | 0 | File a complaint (`complaint`), Give item to NPC (`delivery`), Record medical data (`medical_record`) |

“STO Kanban” has an internal ID `sto_kanban`, but the current Russian localization of the name is STO “Kaban”. The remaining sections use the name visible to the player. Actions are called through the interface; the list of identifiers is not a command shell.

## Appendix F. Position Scales

### Court NChG

| Interface stage | Internal rank | Title |
| --- | --- | --- |
| 1 | 0 | Court Staff Trainee |
| 2 | 1 | Court secretary |
| 3 | 2 | Assistant Court Clerk |
| 4 | 3 | Assistant Judge |
| 5 | 4 | Junior Trial Lawyer |
| 6 | 5 | Trial Lawyer |
| 7 | 6 | Senior Trial Lawyer |
| 8 | 7 | Justice of the Peace |
| 9 | 8 | District Judge |
| 10 | 9 | Chairman of the District Court |
| 11 | 10 | Court of Appeal Judge |
| 12 | 11 | Chairman of the Court of Appeal |
| 13 | 12 | Federal Judge |
| 14 | 13 | State Counsel of the Supreme Court |
| 15 | 14 | Supreme Judge |

### IC NChG

| Interface stage | Internal rank | Title |
| --- | --- | --- |
| 1 | 0 | Trainee Investigator |
| 2 | 1 | Junior Investigator |
| 3 | 2 | Investigator |
| 4 | 3 | Senior Investigator |
| 5 | 4 | Investigator for particularly important cases |

### MVD

| Interface stage | Internal rank | Title |
| --- | --- | --- |
| 1 | 0 | Cadet |
| 2 | 1 | Trainee |
| 3 | 2 | Private |
| 4 | 3 | Junior Policeman |
| 5 | 4 | Policeman |
| 6 | 5 | Senior Policeman |
| 7 | 6 | Corporal MVD |
| 8 | 7 | Sergeant MVD |
| 9 | 8 | Senior Sergeant MVD |
| 10 | 9 | Ensign MVD |
| 11 | 10 | Senior Warrant Officer |
| 12 | 11 | Junior Lieutenant |
| 13 | 12 | Lieutenant |
| 14 | 13 | Senior Lieutenant |
| 15 | 14 | Captain |
| 16 | 15 | Major |
| 17 | 16 | Lieutenant Colonel |
| 18 | 17 | Colonel |
| 19 | 18 | Colonel II rank |
| 20 | 19 | Major General |
| 21 | 20 | Lieutenant General |
| 22 | 21 | Colonel General |
| 23 | 22 | Deputy Minister of Internal Affairs |
| 24 | 23 | First Deputy Minister |
| 25 | 24 | Minister of Internal Affairs |

### UG "Barricade"

| Interface stage | Internal rank | Title |
| --- | --- | --- |
| 1 | 0 | Young |
| 2 | 1 | Bull |
| 3 | 2 | Greyhound |
| 4 | 3 | Rebel |
| 5 | 4 | Blatnoy |
| 6 | 5 | Brother-in-law |
| 7 | 6 | Position 7 (name not specified in technical specification) |
| 8 | 7 | Position 8 (name not specified in technical specification) |
| 9 | 8 | Raid clearance 9 |
| 10 | 9 | Raid clearance 10 |

### ZONASTROY

| Interface stage | Internal rank | Title |
| --- | --- | --- |
| 1 | 0 | Worker |
| 2 | 1 | Bricklayer |
| 3 | 2 | Civil Engineer |
| 4 | 3 | Site Master |
| 5 | 4 | Foreman |

### ChernEnergo

| Interface stage | Internal rank | Title |
| --- | --- | --- |
| 1 | 0 | Electrician |
| 2 | 1 | Equipment Technician |
| 3 | 2 | Senior Technician |
| 4 | 3 | Operating Engineer |
| 5 | 4 | Senior Engineer |

### ComNet NChG

| Interface stage | Internal rank | Title |
| --- | --- | --- |
| 1 | 0 | Radio technician |
| 2 | 1 | Signalman |
| 3 | 2 | Senior signalman |
| 4 | 3 | Network Coordinator |
| 5 | 4 | Senior Coordinator |

## Appendix G. Organization reference cards from technical specification

This section is the contents of the installed directory. Mention of a base, task, form or machine here does not confirm the physical creation of the corresponding resource in the world. For ready-made actions, refer to the main text and Appendix E.

### ZONASTROY

Location: Industrial zone "Oktyabrskaya", eastern outskirts of Pripyat.

Catalog transport: KAMAZ concrete mixer; Excavator EO-3323; Crawler crane KS-4561; Engineering staff pickup; Armored car "Miner".

Catalog objectives: Construction and restoration of buildings NChG; Creation of new fortifications, checkpoints and bridges; Construction of protective domes and underground shelters; Cooperation with ChernEnergo and ComNet in the construction of energy and communication networks; Repair of strategically important facilities after emissions.

### ChernEnergo

Location: Main electrical substation "Radar-3", north-east of Pripyat, underground level of the complex.

Catalog transport: Rotational UAZ “Energia”; Truck GAZ-3308; Mobile power station PES-3; Buggy for patrolling high-voltage routes.

Catalog objectives: Maintenance and restoration of the energy network NChG; Providing power to bases, antennas and laboratories; Repairing lines after emissions and battles; Creation of temporary energy fields of protection; Cooperation with ComNet and MonolitStroy during the construction and connection of facilities.

### ComNet NChG

Location: Abandoned radio complex "Vector-5", south of the city of Yantar.

Catalog transport: Radio van “Avalanche”; SUV with antenna complex; Small reconnaissance drones; Boat for communication in coastal areas.

Directory tasks: Maintaining radio communications between bases and patrols; Monitoring of anomalous radio signals and psi waves; Restoration of satellite channels; Encryption and decryption of faction messages; Support from ChernEnergo and MonolitStroy when installing new antennas.

### Court NChG

Location: Court building NChG in the central part of Pripyat, near Independence Square.

Catalog vehicles: Audi A6 (official vehicle of the judge); Volkswagen Passat (office work); UAZ “Bukhanka” (convoy transport); Mercedes-Benz S-Class (chairman of the court).

Objectives of the catalog: Conducting court hearings on cases transferred from IC and the Prosecutor's Office; Making judgments and decisions based on evidence; Ensuring fair and impartial proceedings; Monitoring the execution of court decisions through bailiffs; Maintaining a register of cases and verdicts, accessible only to government agencies; Possibility of reviewing cases on appeals and complaints; Protecting the rights of citizens NChG and maintaining the rule of law throughout the territory.

### IC NChG

Location: Former administrative complex No. 14 in the central sector of Pripyat (rumored to be the former KGB headquarters).

Catalog transport: Toyota Land Cruiser 200 (armored car IC); UAZ Patriot (task force); Mercedes-Benz E-Class (investigator's official car); Mi-8 helicopter IC (rarely, only by order of the head).

Objectives of the catalog: Conducting interrogations, searches and detentions of suspects in cases NChG; Conducting criminal cases against lawbreakers and corrupt officials; Monitoring the actions of FSIN, traffic police, military and customs for abuse of authority; Gathering intelligence about criminal gangs and artifact dealers; Conducting special operations jointly with other structures (order of the President); Reporting to the Security Council NChG and the President personally.

### SChS

Location: Secret bunker in the area of the destroyed factory.

Style: Regular clothing, hidden equipment.

Catalog transport: Unrated minibus; Civil vehicles.

Catalog objectives: Exploration; Surveillance; Infiltration into groups; Arrests on suspicion of treason.

### Prosecutor's office NChG

Location: Pripyat, building with the coat of arms of the prosecutor's office.

Transport catalogue: Volkswagen Touareg; Toyota RAV4; Toyota Land Rover; Toyota Land Cruiser 200 (tinted); Mercedes-Benz E200 (blue, "Prosecutor's Office" inscription).

Catalog equipment: Suits with shoulder straps; Prosecutor's office cap; Shiny shoes.

Catalog weapons: M-16 (for ordinary prosecutors); PM with a silencer (for ordinary prosecutors); MSG-V1 with silencer (senior prosecutors); USP with silencer (senior prosecutors); Teg 9, improved 24-round version (Chief Prosecutor); MP-7 with adjustable optics (chief prosecutor).

### Service station "Boar"

Location: Area at the junction of the Landfill and Equipment Cemetery.

Catalog transport: ZIL-131 with a workshop body; UAZ 452 (“Loaf”) with “STO” stickers; Pickup trucks with the “Boar” logo; Moskvich 412; Lada 2107 with reinforced suspension; Converted armored personnel carrier (mobile base in dangerous areas).

Catalog objectives: Repair and tuning of weapons and vehicles; Production of modified equipment; Trade in parts, PDA, tools; Black market - possibly illegal weapons ordered by OCG; Maintaining neutrality between factions; Participation in the shadow auction “Rare Artifacts”.

Catalog equipment: Work overalls; Leather apron; Gloves; Sometimes body armor under clothing; Colors: black and yellow elements, boar logo on the back; Senior technicians wear welding masks with modified NVGs.

Catalog weapons: Sawed-off shotguns; PP "Bison"; "Ksyukha"; MP-5; Administrative Code-74M with a grenade launcher (for masters); RPK (for base defense); Nail guns; Electroshock mines; Custom traps based on batteries and spare parts.

Features of the catalog: Know all the secret passages and bookmarks in the Landfill; They can “roll back” the player’s PDA, erase traces or find any log; Own radio frequency “Techno-01” (only for wild boars) and “Techno-00” (for wild boars, subbers and operators).

Additionally: Mobile service stations in Zaton, at Agroprom and sometimes even in the Red Forest; “Black Hangar” is a secret place for tuning experimental vehicles.

### Subbers

Location: Landfill, flea market, not far from the depot, towards the “PMC X-soldiers” base.

Base: Sound center "Dog".

Catalog objectives: Installation and pumping of subwoofers in official, bandit and civilian cars.

Catalog equipment: Stalker overalls, smeared in fuel oil, like the brothers from the Kaban service station.

### UG "Barricade"

Location: Busy metro station.

Style: Leather jackets, masks, red headbands.

Transport catalogue: Buses with barricades; Cars with loudspeakers.

### Operators

Location: Depot, railway station, airfield.

Style: Overalls, driver's paraphernalia.

Transport catalogue: Trains; KamAZ trucks; Taxi; Helicopters.

Catalog objectives: Control over logistics - drivers, machinists, pilots.

### Fanatics

Location: Center of the Zone, old temples, antennas.

Style: Robo-religious, masks, monolith symbolism.

### PMC X-soldiers

Location: Closed camps with helipads.

Style: Modern equipment, mercenaries.

Catalog transport: armored personnel carriers; Military jeeps.

### Veteran snipers

Location: Old military bases.

Style: Camouflage, balaclavas, long-range.

Transport catalogue: UAZ; Motorcycles.

### Clear guys

Location: Ruins of a shopping center or train station.

Style: Adidas, gold chains, cormorants.

Catalog transport: Basins; E34; 2107.

### Stalkers

Location: Villages, temporary camps.

Style: Everything, from sweatpants to armor.

Catalog transport: Everything they find - motorcycles, old UAZs.

### TO "Punisher"

Location: Abandoned morgues and psychiatric clinics.

Style: Medical gowns smeared with blood.

Catalog transport: Pick-up trucks with skull symbols.

### TS “Zone of Power”

Location: Abandoned prisons and camps.

Style: Prison tattoos, peacoats.

Transport catalogue: Trucks; Armored cars with wrist cutting.

### Corruption syndicate

Location: Luxury houses, business centers.

Style: Suits, sunglasses, expensive watches.

Transport catalogue: BMW; Lexuses; Premium class.

### Technobandits

Location: Destroyed research institutes.

Style: Welding helmets, body kit with wires.

Catalog transport: Homemade armored cars.

### TO "Black Cobra"

Location: Mountains and mines where it is impossible to detect.

Style: Black headbands, cobra signs.

Catalog transport: Camouflage pickups; Motorcycles.

### Sector “0”

Location: Underground server rooms, encrypted headquarters.

Style: Tactical clothing and electronic devices.

Catalog transport: Black minivans without numbers.

### Iskra Group

Location: Old power plant.

Style: Firefighter uniform with skulls.

Catalog transport: Homemade buggies; Pickup trucks with flamethrowers.

### Police

Location: Newcomer Village (police station).

Style: 90's uniform, caps, batons.

Transport catalogue: VAZ 2114; UAZ "Loaf".

### MVD

Location: Commissariat in a large populated area.

Style: Classic police uniform.

Transport catalogue: LADA Priora; UAZ; SUVs.

Catalog objectives: Crime investigation; Collection of dossiers; Traffic control.

### FSIN

Location: Maximum security camp in the northwest of the map.

Style: Blue and gray uniform with body armor.

Transport catalog: KamAZ for transporting prisoners; GAZelles.

### Scientists

Location: Yanov Laboratories, Ozerny Bunker.

Style: Chemical protection, scientific clothing, glasses.

Catalog transport: UAZ with trailer; Armored VAZ 2131.

### MChS

Location: Fire station in Zaton/Janow.

Style: Orange uniform, helmets, tools.

Catalog transport: KRAZ “Firefighter”; UAZ; Boats.

### Ministry of Health

Location: Laboratory and mobile hospitals.

Style: White and green uniform, honey. equipment.

Catalog transport: Intensive care units based on UAZ; Trucks with medicines.

### Killers

Location: Abandon hostel in the forest or an abandoned hotel.

Style: Dark jackets, hidden weapons, masks.

Transport catalogue: Black BMW E38; Motorcycles.

### OMON

Location: Base in a dilapidated administrative building.

Style: Classic uniform, helmets, shields.

Transport catalogue: VAZ 2114 “Police”; Bus PAZ; Ural with bars.

### Pennant

Location: Underground command center under the laboratory territory.

Style: Elite equipment, muted colors.

Catalog transport: Camouflage GAZ "Tiger"; Black Gelendvagen.

### Alpha

Location: Closed military base on the border of the zone.

Style: Black uniform with tactical gear.

Transport catalogue: Armored UAZ Patriot; Mi-8 helicopter; Armored personnel carrier.

### Civilian

Location: Secret. Only business government agencies and NBZ employees have access to these accounts.

## Appendix H. Criminal Code: 35 offenses

| Number | Section | Description | Config Sanction | repeat flag |
| --- | --- | --- | --- | --- |
| 1.1 | uk_1_1 | Causing bodily injury to a citizen | Imprisonment for 3 legal years | 0 |
| 1.2 | uk_1_2 | Causing bodily injury to a government employee. structures | Imprisonment 5 legal years | 0 |
| 1.3 | uk_1_3 | Murder of a citizen with a firearm | Imprisonment 5 legal years; Withdrawal of license | 0 |
| 1.4 | uk_1_4 | Murder of a government employee. structures with firearms | Imprisonment 5 legal years; Withdrawal of license | 0 |
| 1.5 | uk_1_5 | Murder by negligence (with fists) | Imprisonment for 3 legal years | 0 |
| 1.6 | uk_1_6 | Attack on VIPs | Imprisonment 5 legal years | 0 |
| 2.1 | uk_2_1 | Hooliganism | Imprisonment for 2 legal years | 1 |
| 2.2 | uk_2_2 | Damage to the state transport | Imprisonment for 2 legal years | 1 |
| 2.3 | uk_2_3 | Insulting government employees structures | Imprisonment for 3 legal years | 1 |
| 2.4 | uk_2_4 | Insulting dignitaries | Imprisonment 5 legal years | 1 |
| 2.5 | uk_2_5 | False information: impersonating a government employee | Imprisonment for 2 legal years | 1 |
| 2.6 | uk_2_6 | Threats of violence or physical harm | Imprisonment 1 legal years | 1 |
| 2.7 | uk_2_7 | Threats of violence against high-ranking officials and government employees. structures | Imprisonment for 4 legal years | 1 |
| 3.1 | uk_3_1 | Terrorist act: shooting people on the street, taking hostages | Imprisonment 5 legal years | 0 |
| 3.2 | uk_3_2 | Weapon sales | Imprisonment for 3 legal years | 0 |
| 3.3 | uk_3_3 | Carrying open weapons is regarded as terrorism | Imprisonment 5 legal years | 0 |
| 4.1 | uk_4_1 | Offering a bribe to an official | Imprisonment for 3 legal years | 0 |
| 4.2 | uk_4_2 | Taking a bribe by an official | Imprisonment 5 legal years; Dismissal | 0 |
| 4.3 | uk_4_3 | Release from custody for bribery | Imprisonment 5 legal years; Dismissal; Emergency organizations | 0 |
| 5.1 | uk_5_1 | Penetration into army territory | Imprisonment for 4 legal years | 0 |
| 5.2 | uk_5_2 | Staying in the FSB office unaccompanied by an FSB officer | Imprisonment for 3 legal years | 0 |
| 5.3 | uk_5_3 | Staying on FSB territory unaccompanied by an FSB officer | Imprisonment for 3 legal years | 0 |
| 5.4 | uk_5_4 | Being in a closed service parking lot near the building MVD without being accompanied by an employee MVD/FSB | Imprisonment for 3 legal years | 0 |
| 6.1 | uk_6_1 | Insubordination | Imprisonment 1 legal years | 1 |
| 6.2 | uk_6_2 | For repeated insubordination | Imprisonment for 3 legal years | 1 |
| 7.1 | uk_7_1 | Sale or use | Imprisonment 5 legal years | 0 |
| 7.2 | uk_7_2 | Storage | Imprisonment 5 legal years | 0 |
| 7.3 | uk_7_3 | Storage of stolen materials | Imprisonment for 2 legal years | 1 |
| 8.1 | uk_8_1 | Vehicle theft | Imprisonment for 2 legal years | 1 |
| 8.2 | uk_8_2 | Theft or attempted theft of military equipment | Imprisonment 5 legal years | 0 |
| 9.1 | uk_9_1 | Complicity in a crime: from 1 to 5 years in prison, depending on the crime charged | Imprisonment 1–5 legal years | 0 |
| 10.1 | uk_10_1 | Leaving the scene of an accident | Imprisonment for 3 legal years | 0 |
| 10.2 | uk_10_2 | Creating a situation for an accident | Imprisonment for 2 legal years | 1 |
| 11.1 | uk_11_1 | Sale of military equipment | Imprisonment 5 legal years; Fine 25,000 ₽ | 0 |
| 11.2 | uk_11_2 | Illegal trafficking of weapons and ammunition, as well as theft of weapons or ammunition | Imprisonment 5 legal years | 0 |

## Appendix I. Administrative Code: 18 compositions

| Number | Section | Description | Config Sanction | repeat flag |
| --- | --- | --- | --- | --- |
| 1.1 | ak_1_1 | Mat in a public place | Fine 5,000 ₽ | 1 |
| 1.2 | ak_1_2 | Aggression against citizens | Fine 10,000 ₽; Arrest 1 game hour | 1 |
| 1.3 | ak_1_3 | Provocations to rallies | Fine 25,000 ₽; Arrest 2 game hours | 0 |
| 2.1 | ak_2_1 | Speeding | Fine 8,000 ₽ | 1 |
| 2.2 | ak_2_2 | Drive on red | Fine 10,000 ₽ | 1 |
| 2.3 | ak_2_3 | Escaping the chase | Arrest 3 game hours | 1 |
| 2.4 | ak_2_4 | Driving without a license | Fine 25,000 ₽; Arrest 2 game hours | 1 |
| 3.1 | ak_3_1 | Penetration into a protected area | Arrest 2 game hours | 1 |
| 3.2 | ak_3_2 | Setting up a camp without permission | Fine 15,000 ₽ | 1 |
| 3.3 | ak_3_3 | Trading without a license | Fine 20,000 ₽ | 1 |
| 3.4 | ak_3_4 | Wearing a state uniform. structures without permission | Arrest 4 game hours | 0 |
| 4.1 | ak_4_1 | Refusal to present documents | Fine 5,000 ₽ | 1 |
| 4.2 | ak_4_2 | Escape upon inspection | Arrest 2 game hours | 1 |
| 4.3 | ak_4_3 | Provocation of employees | Fine 15,000 ₽; Arrest 1 game hour | 1 |
| 4.4 | ak_4_4 | Violation during inspection | Fine 10,000 ₽ | 1 |
| 5.1 | ak_5_1 | Abandoned vehicle in the wrong place | Fine 7,000 ₽ | 1 |
| 5.2 | ak_5_2 | Using a loudspeaker for no reason | Fine 3,000 ₽ | 1 |
| 5.3 | ak_5_3 | Unauthorized installation of a checkpoint | Arrest 3 game hours | 1 |

## Appendix J. Financial Rules: 19 compositions

| Number | Section | Description | Config Sanction | repeat flag |
| --- | --- | --- | --- | --- |
| 1.1 | fp_1_low | Violation of the ban on disclosing internal information of government agencies | Dismissal | 0 |
| 1.2 | fp_1_high | Draining of confidential information from government agencies | Arrest 3 game hours | 0 |
| 2.1 | fp_2_low | Repeated violation of the mandatory wearing of uniform on duty | Reprimand | 1 |
| 2.2 | fp_2_high | Deliberate disregard for mandatory wearing of uniform | Demotion | 1 |
| 3.1 | fp_3_low | Lack of official ID | Arrest 1 game hour | 1 |
| 3.2 | fp_3_high | Refusal to present official identification upon request | Dismissal | 0 |
| 4.1 | fp_4_low | Bribe up to 10,000 rubles | Arrest 2 game hours | 1 |
| 4.2 | fp_4_high | Bribe over 10,000 rubles | Arrest 4 game hours; Dismissal | 0 |
| 5.1 | fp_5_low | Obscene speech towards senior ranks | Reprimand | 1 |
| 5.2 | fp_5_high | Direct conflict with superiors | Demotion | 0 |
| 6.1 | fp_6_low | Going on duty while intoxicated, first offense | Demotion | 1 |
| 6.2 | fp_6_high | Going on duty while intoxicated, repeated violation | Dismissal; Arrest 1 game hour | 0 |
| 7.1 | fp_7_low | Artifact discovered in the possession of a civil servant | Arrest 3 game hours | 1 |
| 7.2 | fp_7_high | Repeated violation of the ban on storing artifacts | Dismissal; Arrest 4 game hours | 0 |
| 8.1 | fp_8_low | Transfer of weapons to a civilian | Arrest 2 game hours; Dismissal | 0 |
| 9.1 | fp_9_low | Lack of report or video recording of the special operation | Reprimand | 1 |
| 9.2 | fp_9_high | Repeated failure to comply with the obligation to record special operations | Demotion | 1 |
| 10.1 | fp_10_low | Using special equipment without reason | Arrest 1 game hour | 1 |
| 10.2 | fp_10_high | Repeated use of special equipment without permission | Dismissal | 0 |

The sanctions are given as a catalogue. The case still requires authority, trial stage and verified evidence. The repeat flag does not automatically double any NPC sanction. FP4 amount is not available in the normal flow of cases. Descriptions of the Constitution contain 8 chapters and are reference data, without automatic execution of all norms.
