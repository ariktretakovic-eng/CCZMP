[Русский](../../../../snapshot-2026-10-28/02_%D0%AD%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0_%D0%BF%D1%80%D0%BE%D0%BC%D1%8B%D1%88%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C/CCZMP_ECONOMY_INDUSTRY_TECH_SPEC_v1.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# STALKER X CCZMP - Technical Specification for Economics, Commerce and Industry

**Document:** CCZMP-ECO-TECH-001 · **Version:** 1.0 (project technical specification) · **Date:** 10/17/2026 · **Language:** Russian · **Encoding:** UTF-8  
**Purpose:** transfer to developers and AI agents as a single contract for the implementation of **mechanisms**, and not an artistic RP-scenario.  
**Basis:** ongoing dialogue about the auto industry, material economics and property + user submitted materials.  
**IMPORTANT:** this document describes the **target architecture**, not the finished implementation. It deliberately separates established facts, author's decisions, design proposals and unknown parameters.

## 0. Reading rules, degree of reliability

Tags: **[AUTHOR]** - directly formulated user requirement; **[SOURCE]** - statement from the attached materials (can describe the lore, plan or state of a separate assembly); **[PROJECT]** - a specific proposed engineering method for fulfilling the requirement; **[CHECK]** - cannot be accepted as an established fact without verification; **[NOT IMPLEMENTED]** - lack of confirmation of a working system.

In case of conflict of texts, priority: **direct last decision of the author → current technical check on the working assembly → previous author's concept → old AI proposals**. You cannot turn proposed brands, prices, balances, resources and algorithms into the “official canon” without approval. **In the user dialogue NAZ is named as the author; the remaining names of six auto companies were suggested by the assistant and remain working.**

### 0.1 Primary sources

| Code | Document | Application/Validity |
|---|---|---|
| SRC-01 | `CCZMP_объединённый_очищенный.txt` | Institutions, NChG, Chernobyl ruble, enterprises, banks, industries; mixes plot and mechanic sketches |
| SRC-02 | `STALKER_X_CCZMP_MASTER_CONCEPT-1.md` | Goals, offline/online, real estate, economics, transport; clearly marked with concept |
| SRC-03 | `CCZMP_technical_guide.md` | A snapshot of the actually described offline assembly as of 10/08/2026 with a list of restrictions |
| SRC-04 | `CCZMP_items_hacking_guide.md` | Description of a separate subject engineering segment as of 10/09/2026 is not equal to the complete physical industry |
| SRC-05 | `CCZMP_items.pdf`, `CCZMP_items_v2_предложения.pdf` | Product catalogs and offers; NOT automatically confirmed implementation |
| SRC-06 | `CCZMP — транспорт организаций по рангам.pdf` | Departmental demand and transport assignments; some models are proposed, ranks are sometimes assumed |
| SRC-07 | `CCZMP_transport_models_sources.xlsx`, `cczmp_models_foreign.md` | Catalog of donor models; links and licenses subject to verification |
| SRC-08 | `cczmp_site_merged.html` | Existing HTML layout/interface artifact, not considered a ready-made banking or industrial server system |
| SRC-09 | Dialogue 10/17/2026 | Priority functional requirements of industry, automotive industry, commercial property |

## 1. Scope and mandatory invariants

**[AUTHOR]** Develop the NChG economy not as a crafting menu, but as a system with a traceable physical origin of resources and products. The player has the right to **create, acquire, sell, donate, transfer, inherit according to the rules of the world, reorganize** companies and industrial complexes: quarries, mines, processing plants, power plants, component factories, assembly plants, concerns and other industrial enterprises. Mined reserves are finite; new reserves are found through geological exploration or come in the form of reliably recorded imports. Each type of production has material, energy, infrastructure and technological prerequisites.

**Hard technical invariants for industrial mode**:

1. `SUM(израсходовано + потери + остаток) == SUM(приход)` within the declared accuracy of each accounting value; The material balance is checked transactionally.
2. Regular release of an item is only possible from **reserved and then scrapped** input lots per approved recipe/BOM, subject to availability of production capacity, energy, conditions and working hours. Administrative/debug spawning is only allowed in an **isolated test economy** with an audit and without recording it as normal production.
3. You cannot sell/ship/spend one shipment twice; every operation is idempotent.
4. The transfer of ownership does not create or destroy a resource and should not automatically transfer someone else's debts without the provided type of transaction.
5. Each field has a final accounting of recoverable reserves; exploration reveals pre-determined or reproducibly generated geological data **before production**, and does not restore already consumed reserves.
6. All commercial and warehouse operations are protected from parallel conflicts; in online mode, the final decision is made by the server.
7. World business processes continue to be calculated when the level is not loaded. In offline events are recalculated according to the local save time; online - server simulation time.
8. The origin report shows the chain “product → batches of components → batches of raw materials → extraction/import/recycled materials”; We don't physically create a separate X-Ray object for each molecule or nut.
9. Connecting the system does not break existing Lua modules, saves, F6/F7, bank and documents; versioned migration and the ability to disable the module are required.
10. All production parameters are externally configurable; calculations are deterministic given the same inputs/seed/directory version.

**The limit of a fair simulation:** “not a speck of dust from the air” is a principle of accounting, not a promise of an atomistic simulation. Materials are aggregated into batches (mass/pcs/l/kWh, etc.), losses go into clearly classified waste/emissions/heat; free energy flow and ideal 100% output are prohibited unless justified by the model.

## 2. Base world and platform limitations

- **[SOURCE]** NChG - Independent Chernobyl State. The currency in one of the constitutional drafts is **Chernobyl ruble (CR)**. In other files, prices are indicated “₽”; **the unit of account and the rate need to be standardized**, these signs should not be automatically accepted as equal.
- **[SOURCE]** International trade links/imports are conceptually provided for; the story names China, India, Estonia and EU countries. This is the basis for simulated foreign trade, but **not proof of an implemented international interface**.
- **[AUTHOR]** Production profile NChG is a hybrid of Soviet industrial heritage and modern technology: UAZ/Ural and historical cars of the 1930s-1940s next to modern UAVs, cars, radars and aviation. Production technologies and product quality vary across companies and eras.
- **[SOURCE]** Main known base: S.T.A.L.K.E.R. Anomaly 1.5.1 / X-Ray (Monolith Engine); online is still target, not confirmed. Offline is the first stage; single logical online world with a target of 1000-2000 players - **target, unreached capacity**.
- **[PROJECT]** Calculated economic model - a separate layer (Lua adapter offline; separate server core with a transactional database in the future online). The engine is responsible for the physical interface, nearby objects and visualization; do not force CCar/ALife to act as the sole database of the enterprise.

## 3. Subsystem map and API contracts

```text
Geology/Resources ─┐
Imports/Salvage ────┼→ Inventory/Lots → Production/Recipes → QA/Products → Warehouses/Logistics → Market/Consumers
Equipment/MRO ─────┤         ↑                  ↑                    ↑                      ↑
Energy/Water ───────┤         │                  │                    │                      │
Workforce/Skills ───┘         └── Companies/Assets/Ownership ─────── Finance/Contracts/Bank
                                      │             │                         │
                                Licensing/Tax    R&D/IP                 Audit/Legal
                                      └─────────────┴───────────→ X-Ray integration / UI
```

Suggested independent modules: `eco_core`, `eco_catalog`, `eco_geology`, `eco_inventory`, `eco_recipes`, `eco_equipment`, `eco_factory`, `eco_utilities`, `eco_logistics`, `eco_market`, `eco_company`, `eco_property`, `eco_finance`, `eco_law`, `eco_rnd`, `eco_vehicles`, `eco_ai_bridge`, `eco_xray_adapter`, `eco_persistence`, `eco_audit`. Each module provides a *stable API*, data schema, events and tests. Modules cannot be integrated by gluing together global Lua tables with random access to someone else's state.

### 3.1 API Agreements [Draft]

- UUID/ULIDs as strings; `schema_version`, `config_version`, `created_at_tick`, `updated_at_tick`, `owner_id`, `audit_id` where applicable.
- Units: mass **kg**, volume **m³**/**l** with explicit conversion, energy **kWh**, power **kW**, time - **simulation ticks** and conversion to game hours, money - **integer number of minimum monetary units** (without float).
- The quantity is stored in fixed decimal precision / integer base units, rather than in binary `float`.
- Commands: `validate → reserve → commit/rollback → emit event`; commands have `command_id` and `expected_version`, events have `event_id` and `causation_id`.
- Example events: `DepositSurveyed`, `OreExtracted`, `LotCreated`, `LotSplit`, `LotConsumed`, `MachineBroken`, `PowerCurtailment`, `ProductionStarted`, `ProductionFinished`, `ProductRejected`, `ShipmentDispatched`, `ShipmentDelivered`, `OwnershipTransferred`, `InvoiceSettled`, `VehicleCertified`.
- The event bus is sufficient at the interface/local log level; Kafka and microservices are **optional** for offline and early prototyping.

## 4. Industries: not only cars

| Level | Subsector | Examples of created assets | Inputs → Outputs |
|---|---|---|---|
| 0 | Geological exploration | laboratory, drilling party, exploration license | fuel, work, instruments → confirmed reserves |
| 1 | Extraction | iron/copper/limestone/sand quarry, mine | reserves, equipment, energy → ore/rock |
| 2 | Enrichment | crushing site, factory | ore, water, reagents → concentrate/tailings |
| 3 | Metallurgy | blast furnace, steel smelting, rolling mill | concentrate/scrap, flux, energy → alloy/rolled/slag |
| 3 | Chemistry/petroleum refining | Refinery, production of polymers, oils, coatings | oil/gas/intermediates → fuels, plastics, coatings |
| 3 | Construction materials | cement, glass, concrete, brick factory | limestone, sand, clay, energy → materials |
| 4 | Accessories | bearing, cable, battery, tire, electronic factories | semi-finished products → components/components |
| 5 | Machine tool industry | CNC machines, tool factory | metals, components, electronics → equipment |
| 6 | Assembly | automobile, railway, agricultural, aviation/special equipment | components/energy → products |
| 7 | Services | Service station, logistics, dealer, builder, energy network, communications | labor/resources/capacity → services/displacement |
| 8 | Recycling | dismantling, metallurgical recycling | defect/scrap/old property → recyclable materials/waste |

**Do not assert** historically unrealistic spontaneous generation of a full cycle: the import of finished machines and primary components is allowed as a verifiable source during the initial deployment of the world. Starting assets of the economy are formed by a **versioned seed manifest** with origin and audit event `WorldBootstrap`, and are not “issued” daily from the menu.

## 5. Geology and production

### 5.1 Entities

`Deposit(id, geometry_ref, resource_type, grade_distribution, in_situ_mass, proven_mass, recoverable_mass, remaining_recoverable_mass, overburden_mass, depth, hazards, survey_state, depletion_state)`; `MiningPermit(id, deposit_id, licensee_company_id, start/end, extraction_limit, environmental_constraints)`; `Pit(id, land_right_id, operator_company_id, equipment_ids, roads, utility_connections, status)`; `ExtractionJob(id, deposit_block_id, input_energy, machine_hours, gross_tonnes, ore_tonnes, waste_tonnes, loss_tonnes)`.

- Land plot, subsoil use right, quarry equipment and enterprise are **different** objects of law. When selling company shares, a state-owned deposit cannot be automatically considered sold.
- Geological blocks store individual indicators of content, moisture, depth, accessibility and quality. Extraction is limited by the minimum balance, equipment productivity, energy, shifts, removal and permitted volume.
- Exhaustion mechanism: `remaining := remaining - extracted`; repeating a request with the same `command_id` does not write off again. “New” deposits should not appear in a depleted block. Creating a new quarry - obtaining rights to an **already existing** resource and deploying equipment.
- Ores and waste rock go into different batches, extraction and losses are recorded. For imports, a specific external delivery is issued with a document of origin, price and delivery time.

### 5.2 Example config (schematic, not ready for the engine)

```yaml
id: dep_iron_pripyat_017
resource: iron_ore
units: kg
proven_recoverable: 2500000000
remaining_recoverable: 1834500000
blocks:
  - id: block_a
    recoverable: 850000000
    fe_fraction: 0.58
    mining_difficulty: 1.35
licensee: company_example_024
status: surveyed
```

### 5.3 Acceptance conditions

Cannot extract > remainder; cannot mine without a valid license/equipment; parties record origin; after depletion and restart, the balance is not restored; simultaneous applications do not bring the balance below zero.

## 6. Materials, batches, BOM and technical processes

**The main inventory unit is a batch (`lot`)**, not an engine object. Each batch has `material_id`, `quantity`, `unit`, `quality`, `origin_ref`, `owner_id`, `location_id`, `encumbered_qty`, `reserved_qty`, `version`. For unique machines, engines and VIN cars - serialized individual copies; components of mass production - in batches.

**Material receipt**: extraction, legal import, dismantling of property/processing, adjustment by migration only with administrative audit. **Material consumption**: production, repair, construction, destruction, waste, export, consumption. Any adjustment must have a document and a reason code.

### 6.1 Recipe Specification [DRAFT]

```yaml
recipe_id: cczmp_auto_brake_disc_v1
product: auto_brake_disc
output_qty: 1
inputs:
  - {material: cast_iron_blank, qty: 8, unit: kg}
  - {material: machining_tool_wear, qty: 0.01, unit: wear_units}
utilities:
  electricity_kwh: 4
  process_water_l: 2
requirements:
  machine_types: [cnc_lathe, balancing_station]
  qualified_role: machinist
  blueprint_id: blueprint_brake_disc_v1
process_time_minutes: 35
outputs:
  - {material: auto_brake_disc, qty: 1, unit: pcs}
  - {material: metal_chips, qty: 2, unit: kg}
  - {material: scrap_rejects, qty: 0, unit: kg}
# NOTE: числа демонстрационные, инженерной верификации нет.
```

**Quality Rule:** actual alloy composition/tolerance/equipment condition, qualification and quality control determine the result; defective products have their own status and can be processed, destroyed or sold in a legal way with the disclosure of the defect. Do not introduce defect probabilities and standards as absolute without the specification of the technologist.

### 6.2 Production order algorithm

1. `CreateWorkOrder`: Check drawing/authorization, route, capacity, certification, equipment, workshop access and operator's rights.
2. `Plan`: build a DAG of BOM dependencies, evaluate available lots, balances, utility limits, transport.
3. `Reserve`: atomically reserve batches/machine-hours/capacity; it is forbidden to reserve > available.
4. `Start`: check the conditions again; start consumption by technological stages (do not keep the annual consumption volume blocked unreasonably).
5. `Tick`: write off what is actually used, accumulate semi-finished products, heat, waste and wear and tear; if energy is unavailable, pause or perform a safe shutdown.
6. `QualityGate`: take measurements and reject.
7. `Finish`: create output batches with parent links, act, product passport; remove reserves.
8. `Abort/Fail`: document already incurred costs, balances, defects, losses and release of unspent reserves. You cannot roll back the actual expense just because the user clicked “cancel”.

`WorkOrder` status: `draft → planned → reserved → running ↔ paused → qa_pending → completed/partially_completed/rejected/cancelled/failed`.

## 7. Machines and promotional equipment: not buttons

`Machine` = type/model, inventory number, owner, location, technological operations, performance, resource/wear, component condition, calibration, service interval, current task, energy/water/compressed air consumption, safety mode. Machines can be purchased, delivered, installed, connected, reconfigured, repaired, modernized and decommissioned. The absence of a machine prohibits the corresponding operation; the absence of a measuring stand may prohibit the release of a certified unit.

**Levels of detail [DRAFT]**: (L0) aggregated power of the area away from the player; (L1) individual machines and production orders within the busy area; (L2) interactive operations and devices in the workplace. All levels use the same resource/time balances. Outside the core there is **not** modeling the collisions of each conveyor roller.

**Supply of the equipment itself:** machine tool manufacturing - separate production; at the start, machines can be recorded in the bootstrap registry or imported through import, taking into account delivery. Tool wear, maintenance/prep work, spare parts and downtime are associated with the same batches of resources.

## 8. Electricity, fuel, water, communications and construction

**[SOURCE]** `ЧернЭнерго` (that’s what it says in the attached text, not CherngEnergo) - Chernobyl Energy Company, base - Radar-3 substation northeast of Pripyat, responsible for networks, factories, facilities. In the plot description, the company is stated to be independent from the government; final legal form and relationship with the Department of Energy require approval.  
**[SOURCE]** `ЗОНАСТРОЙ` - state construction corporation NChG, base - industrial zone "Oktyabrskaya" in the east of Pripyat; builds/restores buildings, fortifications, bridges and cooperates with `ЧернЭнерго`/`ComNet`. There is also **discrepancy `ЗОНАСТРОЙ`/`МонолитСтрой` in the same original descriptions** - do not declare this an identity without the author's decision.  
**[SOURCE]** `ComNet НЧГ` - communications/relays, Vector-5 radio complex south of Yantar.

### 8.1 Energy Grid [DRAFT]

Model - graph: `GenerationUnit → Transformer → Line → Substation → ConsumerConnection`. Nodes have a state, capacity, losses, restrictions, owner, service agreement, accounting point. Electricity is not stored as “bags of energy”: step-by-step generation/load/loss/storage balance model with `kWh` per interval; an unpaid bill does not convert physical energy into negative storage.

Generation: heat/diesel (fuel/cooling), hydroelectric power station (available hydraulic energy), renewable energy sources (input natural flows), **anomalous** generation, if its energy is limited and explained within the game world with clearly defined performance/risks. The production order checks the actual available capacity; the disadvantage gives `paused`/reduced tempo, not free work.

### 8.2 Water and heat [DRAFT]

`WaterSource → PumpStation → Treatment → Pipeline → Consumer → Wastewater`; quality/volume/leakage/pressure/pumping equipment/power supply. Process water can circulate; fresh recharge and losses are taken into account separately. Heat, steam and compressed air are additional networks with their own resource balances.

### 8.3 Construction [DRAFT]

`LandRight → Planning/Permit → BillOfMaterials → SitePreparation → Foundation → Structure → Utilities → Commissioning → AssetRegistration`. Construction consumes materials and man/machine hours, and creates a physical/logical object **only after** the appropriate stages. Availability of geometry types varies by models/SDK; the economic act of construction is not considered evidence of the existence of collisions, doors, rooms and interiors.

## 9. Universal property and commercial activities

**[AUTHOR]** For all industries, the player has the right to establish new companies, buy existing ones, change directions of activity, reorganize, sell, donate, transfer rights, build/acquire enterprises and trade production assets. This applies to quarries, processing/metallurgical/assembly/parts manufacturing plants, generation companies, warehouses, logistics and infrastructure.

### 9.1 Entities [DRAFT]

- `LegalEntity`: id, registered_name, display_name, registration_no, legal_form, status, jurisdiction, beneficial_owners, legal_address, tax_profile.
- `EquityHolding`: entity_id, holder_person_or_entity_id, share_units; sum of shares = 100% or agreed whole number of shares.
- `Asset`: id, category, owner_id, custodian_id, location, state, valuation, liens, restrictions, asset_specific_data.
- `PropertyRight`: asset/land/deposit/equipment/blueprint, owner, basis, valid_from/to, encumbrances.
- `Enterprise`: operating organization, can rent property and **not own** it; `Facility` - a specific site with equipment.
- `License`: issuer, scope, holder, prerequisites, expiry, status; a revoked license stops the activity in question without automatically destroying the property.
- `Contract`: parties, subject, quantity/quality, term, responsibility, security, condition of performance, status; `Invoice`, `DeliveryAct`, `ShareTransfer`, `AssetTransfer`, `Lease`, `Pledge`, `Loan`, `InsurancePolicy`.

**Legally different transactions**: sale of 100% of the company's shares; sale of one plant as a property complex; assignment of license, if permitted; machine sales; plot rental; gift from the company. An implementation must not mix these operations in `change_owner(name)`.

### 9.2 Commands

`RegisterCompany`, `AmendCompany`, `IssueShares`, `TransferShares`, `MergeCompanies`, `SplitCompany`, `LiquidateCompany`, `BuyAsset`, `GiftAsset`, `LeaseAsset`, `PledgeAsset`, `PurchaseIndustrialFacility`, `RegisterLandRight`, `ObtainMiningPermit`, `AcquireEquipment`, `RegisterTrademark`, `FilePatent`, `DeclareBankruptcy`.

**Transfer transaction**: seller/buyer auth → verification of owner/collateral/seizure/restrictions → verification of signatures and conditions → cash reserve/escrow if purchase → atomic change of rights registry → settlement → journal/notifications. In case of an error, no half-transmission.

### 9.3 Antitrust and balance

Players can own holdings and vertically integrated chains. Restrictions on ownership concentration, infrastructure tariffs, taxes and public participation rules - **rules NChG, which must be approved separately**. It is impossible to prohibit the purchase of a “too large” plant without the author’s decision. The system must support both the free market and legally allocated strategic assets.

## 10. Banks, payments, taxes, stock exchange, accounting

**[SOURCE]** The original corpus describes the NBZ - **People's Bank of the Zone** (other transcripts are found in different materials; record one official one); payments/loans/deposits/blocking. **[SOURCE: technical certificate dated 10/08/2026]** in the current offline build, the bank “balance” on F6 reflects the Anomaly wallet, and **there is no full-fledged separate current account and transfers yet**; loans and deposits are limited by existing script logic. **Do not declare industrial banking ready.**

**[PROJECT]** Double entry ledger for all funds. An account balance is a calculated balance of transactions, and not a figure that can be changed arbitrarily. Key accounts: wallet, current account of an individual/company, cash desk, reserve, escrow, tax/state payment, receivable/creditor. `sum(debits) == sum(credits)` by currency for each transaction performed. Borrowings create both an asset and a liability. You cannot pay 2 contracts with one balance under race conditions.

Functions: accounts and powers of signatories; payments and salaries; procurement; lending secured by property; corporate shares/dividends; rent/leasing; insurance of factories, cargo and transport; government tenders, taxes, import duties; audit and bankruptcy. Interest rates, tax brackets and specific pricing formula **not approved** - configurable policy.

The price of a product consists of raw materials/energy/labor costs, depreciation, logistics, taxes, financial costs and the desired margin; **the market price may differ from the cost**, and this is normal. You can't rely on an economic system just to endlessly sell items to NPCs at a fixed price.

## 11. Logistics and warehouses

Warehouse - `StorageLocation`, capacity by weight/volume, environmental restrictions, owner and responsible; batches have storage locations and status (`available`, `reserved`, `in_transit`, `quarantined`, `damaged`, `consumed`). Moving between sites: `ShipmentOrder → Pick/Pack → Load → Transit → Unload → Acceptance`. The move does not create a new batch with “new” material, but rather changes the location/splits up the original batch while preserving the lineage.

The transport contract takes into account the carrying capacity, fuel, route, vehicle condition, driver, loading points and loading equipment. For interlocation transportation, at the first stage, **calculated movement** along a previously verified path is allowed if the physical transport AI is not yet ready; the ban on instant free teleportation persists through duration, costs, cargo capacity and risks. When players are present, vehicles are displayed in the world; transition between levels uses the same shipment.

## 12. Automotive industry NChG - six manufacturers

**Title status**: `НАЗ — Национальный Автопром Зоны` - **[AUTHOR]**. The remaining five - **[PROJECT/WORKS]**, proposed earlier in the correspondence, require approval: `VAREON`, `NEOTERRA`, `НАРОД`, `VARGAN`, `АВТОМИР/АВМ`. **Snow Leopard** is a working version of the national totem/emblem of VAREON, the author did not finally approve it.

| Manufacturer | Niche and role in the system | Engineering Honors |
|---|---|---|
| **NAZ** | Traditional Soviet heritage, ZIS/ZIL/UAZ/Ural-like trucks, historical and service vehicles | Simple platforms, maintainability, large product range, long support cycle |
| **VAREON** *(work)* | Exclusive luxury cars, hypercars, executive limousines | Small series, custom materials, complex QA, manual assembly, expensive components |
| **NEOTERRA** *(work)* | Electric vehicles, autonomous systems, experimental eVTOLs | Batteries, power electronics, software, security system certification, pilot batches |
| **PEOPLE** *(worker)* | Affordable urban transport and inexpensive mass-produced cars | Unification of platforms, low costs, limited versions for urban mode |
| **VARGAN** *(work)* | Modern SUVs, pickups, expeditionary and special vehicles | Drive, transmission, suspension, off-road geometry, modifications |
| **AUTOMIR / AVM** *(work)* | Satirical laggard mass producer | Outdated technologies, high percentage of repairs, price does not necessarily correspond to quality |

**Model ranges are preliminary references only, NOT a register of registered models:** NAZ-110/130/157/410/555/700/900; VAREON S600/S900/Imperium/GT/V12; NEOTERRA E1/E5/E9/Cargo/Pilot/Aero; PEOPLE-1/3/5/7/E/Cargo; VARGAN T4/T6/T8/X900/Expedition/Defender; AVM-2101/2110/2115/2190/Future. Replace matches with real brand names if necessary.

### 12.1 Map of supplier factories

1. Ore quarries, mines, scrap metal and petroleum raw materials → concentration/metallurgy/chemistry/polymers.
2. Sheet steel/aluminum → stamping of body, frames, welded components.
3. Foundry/forging plant → cylinder block, shafts, gears, hubs.
4. Machining/heat treatment/grinding → engine, gearbox, bearings, gearboxes.
5. Electrical/electronic plant → harnesses, ECU, sensors, instruments, chargers.
6. Chemicals/polymers → plastics, sealants, coatings, oils, tires.
7. Glass/textile → glazing, insulation, interior trim.
8. Battery plant → traction and starter batteries; requires a separate chain of active materials and assembly.
9. Service market → supply of machines, molds, equipment, instrumentation and maintenance.
10. Final Assembly → Body Line, Paint, Chassis, Powertrain, Interior, Electronics Calibration, Bench Tests, VIN/Certificate, Finished Goods Warehouse and Dealer.

**Important:** the supplier does not have to belong to the automaker: another player can own a battery factory and sell products to VAREON, NAZ and an independent garage manufacturer. Interchangeability only allows verified standard/compatibility, not string name matching.

### 12.2 Car as a product and asset

`VehicleDesign(id, revision, brand_company_id, type_approval, parts_BOM, geometry_asset_ref, simulation_params, licensing_refs)`; `VehicleUnit(VIN, design_revision, assembly_work_order_id, component_serials, quality_certificate, owner, registration, damage, odometer, maintenance_records)`. Each production car has a unique VIN and associated production history; pre-existing imported vehicles are sourced `imported_vehicle` rather than dummy local build.

**Player’s own brand**: registration of a legal entity and brand → project/drawing → licenses for components and software → BOM and production route → prototype → testing → certification → production series → dealers. **Engine Limit**: Player can combine existing platforms/parameterized parts; arbitrary highly detailed geometry of the new body cannot be guaranteed with one button without an external pipeline Blender/X-Ray SDK and delivery of client assets.

**[SOURCE]** Additional tables contain actual foreign models/departmental assignments (including MVD, IC, OMON) and donor links - use as **original import/service fleet and potential test base**, do not declare NChG as in-house production. For Sketchfab/other catalogs, separately check authorship, license for modification/distribution, rights to brands, asset format and quality.

## 13. Research, competencies and intellectual property

`Blueprint/DesignRevision`, `Patent/License`, `ResearchProject`, `TestReport`, `Certification`, `SkillQualification`. The development of a new material/propulsion system/electronic assembly uses laboratory capacity, equipment, personnel, samples, experimental batches and verifiable calculations. Successful experience gives a **versioned result** (drawing/technological map/config), and not items produced out of thin air. Rights to an industrial design, brand and drawings may belong to a citizen/legal entity and be transferred/licensed.

For deep simulations (electrical circuits, instrumentation, mechanical calculations) you need a **separate mathematical engine or module**, validated on benchmark tests; do not hide arbitrary random numbers under the guise of the laws of physics. Provide basic, professional and expert levels of interaction with equipment.

## 14. Communication with existing institutions and enterprises

| Organization | Confirmed role in sources | Connecting to new APIs |
|---|---|---|
| ZONASTROY | Nation building and reconstruction | Construction orders, building BOM, equipment, acceptance testing, assets |
| ChernEnergo | Power supply and networks | Generation, networks, plant consumption, metering and tariffs |
| ComNet NChG | Communications, repeaters | Object connectivity, production/dispatching connection |
| NBZ | Bank, deposits/loans; still limited implementation | Current accounts, ledger, corporate loans, escrow |
| Ministry of Economy NChG | Economic Regulations, Trade and Fees | Registration/reporting, taxes, licenses within the scope of authority |
| Government departments | Purchase and operation of transport, special equipment | Tenders, procurement, state budget, specifications and supplies |
| "Voice of Pripyat" | Private radio station, advertising/contracts | Commercial services/advertising contracts, payments |

**Title and conflict registry:** `ЗОНАСТРОЙ` has capitalization options `ЗонаСтрой`; `ЧернЭнерго` - exactly the spelling of the original source (mentioned by the user “CherngEnergo” should be considered a typo before approval); `МонолитСтрой` in separate paragraphs intersects with ZONASTROY tasks, identity **not determined**; the decoding of "NBZ" occurs in different contexts and requires one canonical entry.

## 15. Implementation status and compatibility limits (by sources)

**Snapshot confirmed only by documents, not a re-audit today:**

- Technical certificate **08.10.2026**: F6/F7, organizations, limited bank deposits/loans, some actions of organizations and logical infrastructure nodes; "construction" ZONASTROY **registers a logical node**, but does not create a physical building, chamber or power grid.
- Technical certificate **08.10.2026**: separate corporate bank register/full transfers, purchase and registration of a car, physical real estate and industrial system **not implemented** according to this certificate.
- Subject reference **09.10.2026** states the catalogue, engineering recipes and subject interactions; these limited recipes are **not equal** to universal industrial recipes, production workshops, quarry or company ownership.
- Initial PDF/transport lists are often marked “described”, “proposal”, “ranks assumed”; **do not consider the listing as ready-made game code**.
- Not a single attached file proves that the industrial platform described in this technical specification has already been written or tested. The current state requires a new audit of working files `D:\CCZMP PROJECT`.

### 15.1 Integration adapter [DRAFT]

The Lua layer must have clear functions: `eco_init`, `eco_tick(dt_game)`, `eco_command(actor, operation, payload)`, `eco_query(actor, query)`, `eco_save`, `eco_load`, `eco_subscribe`; internal domain implementation should not be bound to F6 UI. Automation actions can be called from a terminal, PDA, dialog, workbench, enterprise or future site through different adapters. Online transfer should preserve domain rules and not copy trust to the client.

## 16. Exploit protection, auditing and save durability

- All significant transactions are initiated by an authorized entity; verify powers, condition of the object, ownership, license term, limits, funds, actual location.
- Idempotency keys and unique restrictions on duplicates: VIN, serial numbers, payments, contracts, work orders, registration numbers.
- Transactional lock/optimistic version for lots, accounts, property and equipment; prohibition of negative balances.
- In online mode, the client does not tell the server “I mined 10 tons” as an authoritative fact: the server recalculates the conditions.
- Audit: `actor`, `device/session`, operation, scheme version, changes, links to documents, time, outcome of the operation; log append-only if possible.
- Reservation and transfer of resources across level boundaries - a single state machine; You cannot receive cargo twice when departing/reconnecting/cancelling.
- Transaction log + snapshots + crash recovery test in the middle of an operation; migrations with schema checking and backup.
- AI code generation passes unit/integration/load/property tests; untrusted automatically generated Lua/SQL configs do not gain access to money and resource release operations without checks.
- The regular game and debug sandbox are isolated by `world_id`. The test spawn does not overlap with the real industrial registry.

## 17. Performance

Do not calculate the detailed physical interactions of all enterprises in all locations. Use **hierarchical simulation**: remote plants = production queues/batches and aggregated capacities; active zone = visible models/animations, only necessary X-Ray objects; player at the machine = in-depth operation. Same sources of condition; Economy LOD changes the calculation frequency/visual detail, but does not provide a free release.

Main restrictions: limited number of events per tick; batch calculation without loss of order; isolated regional queues; snapshots; asynchronous read-model for the interface; autosave with transactional recovery. The 1000-2000 player target requires separate load tests, this is **not a guaranteed feature of X-Ray**.

## 18. Recommended storage scheme [DRAFT]

**Tables:** `worlds`, `accounts`, `characters`, `legal_entities`, `equity_holdings`, `company_roles`, `properties`, `assets`, `encumbrances`, `licenses`, `land_parcels`, `deposits`, `deposit_blocks`, `surveys`, `mining_jobs`, `material_catalog`, `lots`, `lot_genealogy`, `lot_reservations`, `warehouses`, `equipment`, `equipment_maintenance`, `blueprints`, `recipe_versions`, `production_routes`, `work_orders`, `work_order_inputs`, `work_order_outputs`, `quality_tests`, `facilities`, `utility_nodes`, `utility_edges`, `utility_meters`, `vehicle_designs`, `vehicles`, `vehicle_components`, `shipments`, `shipment_legs`, `contracts`, `invoices`, `payments`, `ledger_accounts`, `ledger_entries`, `loans`, `insurance_policies`, `tax_rules`, `tax_obligations`, `research_projects`, `patents`, `audit_events`, `outbox_events`, `schema_migrations`.

Critical constraints: `CHECK(quantity >= 0)`; `UNIQUE(world_id,command_id)`; `UNIQUE(world_id,vin)`; link integrity `owner_id`, `lot_id`, `deposit_block_id`; `SUM(outgoing shares)<=issued shares`; `SUM(postings per transaction)=0` is checked by transactional logic or deferred constraints. Always save `world_id` in offline/online accounting keys.

### 18.1 Example JSON command (format for developers, not actual API)

```json
{
  "command_id": "cmd-001",
  "world_id": "offline-save-01",
  "actor_id": "person-04",
  "type": "StartProduction",
  "payload": {
    "facility_id": "factory-11",
    "recipe_id": "cczmp_auto_brake_disc_v1",
    "recipe_revision": 1,
    "quantity": 10,
    "input_lot_ids": ["lot-iron-19"]
  },
  "expected_version": 7
}
```

```json
{
  "success": false,
  "code": "INSUFFICIENT_STOCK",
  "message": "Недостаточно доступного материала с учётом резервов",
  "audit_id": "audit-0092"
}
```

## 19. End-to-end (E2E) verification scenarios

**T01 - quarry → brake disc → car:** explore and license an ore block; get the final batch; process; transfer to another owner; produce a disc, pass QA; install on car; Using the VIN, trace the genealogy to the quarry. Control: units, waste, revenue, ownership, provenance.

**T02 - energy deficit:** shutdown of ChernEnergo reduces/zeroes available power; the technical process is suspended, the resource is not duplicated; during recovery continues at the correct stage.

**T03 - purchase of an operating plant:** another player buys shares of a legal entity (or a separate asset), checks encumbrances, payment, contract; plant, warehouse lots and licenses are transferred **only where provided for by the type of transaction**.

**T04 - open pit exhaustion:** several parallel applications exceed the balance; the permissible volume is mined once, the rest is rejected; after a reboot, the ore does not return.

**T05 - crash during payment + shipment:** recovery from WAL/log, no duplicate goods, missing money or stuck reserves.

**T06 is an independent car brand:** the company registers a car project, purchases third-party components, produces a prototype, tests, certifies, produces a production car; unique VIN, documents and compatible visual resources.

**T07 - offline in another location:** the player leaves Pripyat, the factory continues to pay; When returned, inventory and production queues match the log.

**T08 - bankruptcy:** there are debts, pledge of machines, rented workshop, other people's goods in warehouse; the procedure does not sell assets not owned by the debtor to third parties.

**T09 - import/recycling:** imported steel has an external document of origin; Scrap metal after recycling a car is included in a new batch, taking into account irreversible losses.

**T10 - compatibility with old build:** F6/F7 work; old loans, documents and cars do not disappear; new modules can be disabled; missing old fields migrate safely.

## 20. AI development plan and integration contract

**The purpose of the AI pipeline:** to assign independent implementations of modules to agents, accept them through tests and then connect them through agreed upon interfaces. AI-generated code is **pre-testing**, not an automatically completed game feature.

**Working order (dependencies are more important than concurrency):**

1. **Phase A: Foundation.** `eco_core` (types/numbers/times/IDs/errors), `eco_catalog`, `eco_persistence`, `eco_audit` + test fixtures, migrations and CI.
2. **Phase B: Material Cycle.** `eco_inventory`/batch, `eco_recipes`/BOM, `eco_factory`/queue, `eco_geology`/depletion; first one product to be tested, not 500 recipes.
3. **Phase C: Finance and Ownership.** `eco_company`, `eco_property`, double entry `eco_finance`, agreements/transactions; NBZ integration only through an adapter, without uncontrolled changes to the old wallet.
4. **Phase D: Infrastructure.** Energy/water, ZONASTROY construction, logistics, component factories.
5. **Phase E: Automotive Vertical Cut.** 1 Factory + 1 Supplier + 1 Car + VIN + Dealer + Purchase; then expand to six brands.
6. **Phase F: Science, markets, trading, holdings.** R&D, patents, contracts, imports, processing, quality.
7. **Phase G: Online.** Replacing the local backend with a server one, checking rights, data migration, load/anti-dump tests.

### 20.1 Standard of result from any developer/AI

Each module is transmitted as: `README` with reservations; `manifest` with version, dependencies, license; description of data objects and interfaces; configs; source code; migration pattern; unit tests and E2E smoke test; startup logs; rollback script; list of unfinished items. **No "implemented" claims unless actual build and play results are included.**

### 20.2 Universal technical specification to a separate AI agent (copy and fill out)

```text
Проект STALKER X CCZMP, база Anomaly 1.5.1 / X-Ray.
Используй CCZMP-ECO-TECH-001 как контракт. Разрабатываем модуль: <MODULE>.
Связи: <INPUT_API> → <OUTPUT_API>. Не модифицируй чужие модули без явной необходимости.
Сделай: исходники, конфиги, схемы/миграции, README, unit и интеграционные тесты,
демонстрационный сценарий, обработку ошибок, audit/event log, rollback.
Инварианты: без создания ресурсов из воздуха; идемпотентность; проверка собственности;
без отрицательных остатков; совместимость со старой сборкой и существующими сохранениями.
Если отсутствует подключение к рабочим файлам, не утверждай, что проверил запуск в игре.
Явно отдели рабочий код от заглушек, неизвестных движковых API и допущений.
Укажи конкретные файлы, команды тестирования, результаты и нерешённые вопросы.
```

## 21. What has not yet been approved (does not block the prototype)

1. Official name, legal form and state shares in five new car brands; totem NChG and emblems.
2. Where exactly will the quarries/mines/factories be located and on what scale will the new industrial zones be displayed?
3. Initial world stocks, volume of imports, population/demand, tariffs, wages, taxes, acceptable legal forms.
4. Simulation time model for pause, sleep, fast forward, server shutdown and world restart.
5. The maximum depth of physical experiments and the order of adding interactive machines.
6. Standard parameters of production recipes: these must be confirmed by a technician/engineer or the selected simulation model.
7. Final decoding of NBZ, ratio CR/₽, canonical spelling ZONASTROY/MonolitStroy.
8. Rules for bankruptcy, strategic assets, alienation of licenses, raiding and operation of monopolies.
9. An authoritative source of wealth after the local economy is transferred online; server stack and engine compatibility require research.
10. Licenses of donor 3D assets, trademarks of real manufacturers, Blender → X-Ray chain and animation quality.

## 22. Definition of Done of the entire platform

The platform is **not ready** if there is only a factory menu or mass spawning of goods. Minimal evidence-based integration: on a clean save, the player acquires a mining permit, extracts the final resource, delivers it to production, spends electricity and machine hours, receives a product with an origin ID, sells it to a company, buys/transfers an enterprise, saves the game, restarts and sees all rights, balances and accounting without duplication. In this case, the lack of supply, energy, operating equipment, ownership or remaining resources must **stop the relevant operation**; All violations are checked by automated tests.

---

### Summary of decision origins

- **Directly approved by the author in this conversation:** diversified factories and supply chains, finite deposits, entrepreneurship/transfer/sale of industrial assets, full-fledged automotive sector, six company specializations, NAZ and the "material origin" ideology.
- **Taken from downloaded materials:** NChG, ChernEnergo, ZONASTROY, ComNet, NBZ, economic context, limitations of the current assembly, various equipment/inventory lists.
- **Proposed engineering implementation:** domain modules, API, transactional database, ledger, `Lot/WorkOrder/Deposit` schemes, state machine, events, tests, phased implementation.
- **Requires approval:** new brands other than NAZ, model lines, national totem, quantitative balances, detailed laws NChG and the final technology stack.
