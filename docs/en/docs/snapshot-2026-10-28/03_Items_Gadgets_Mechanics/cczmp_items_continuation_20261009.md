[Русский](../../../../snapshot-2026-10-28/03_%D0%9F%D1%80%D0%B5%D0%B4%D0%BC%D0%B5%D1%82%D1%8B_%D0%B3%D0%B0%D0%B4%D0%B6%D0%B5%D1%82%D1%8B_%D0%BC%D0%B5%D1%85%D0%B0%D0%BD%D0%B8%D0%BA%D0%B8/cczmp_items_continuation_20261009.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# CCZMP: Items, Hacking, Engineering and Services

Build for an existing project CCZMP / S.T.A.L.K.E.R. Anomaly 1.5.1. Date: 10/09/2026. Base: CCZMP_items.pdf and CCZMP_items_v2_offers.pdf; v2 prices are accepted as game balance. New transport prices and additional rules not included in the documents are indicated separately below.

## What is installed

184 public catalog items: 183 inventory items and a desktop PC; 10 hacking operations, 10 engineering recipes, 6 available ground vehicles and 11 source reference models, licenses and recipes, medical specialists, diseases, protective equipment and weapon customization. Device states, work performed, registry and contracts are saved with the game. Old CCZMP systems are retained.

This is a working game segment, but not a complete visual representation of both documents. The “Remaining” section lists unfinished items; None of the features listed there are considered to be implemented.

## How to open and receive items

- F6 → “Technology, hacking and workshop”: catalog, your devices, operations, recipes, medicine and transport. Actions on the device are also available from the inventory.
- F7 → H or “CCZMP: items and equipment”: debug directory. The item appears in the inventory, desktop PCs and cars appear in the world. Debugging requires starting from `-dbg`.
- Electronics, tools and materials are included in the assortment of Sidorovich, Sych, Flea Market, mercenaries, bandits, mechanics and Sakharov. Sets vary.
- Weapons, ammunition and protective equipment are purchased through a new catalog next to a live friendly merchant, no further than 4 m. Organization and valid physical license are verified. Stock: six packs of cartridges or two units of other goods; recovery after 24 game hours.
- Medicines are sold by a pharmacist, permits are issued by specialized specialists. The item is first created, then the money is debited.
- Empty licenses and recipes from normal spawn do not create a registry entry. To check permissions there is a separate debug output of the current document.

Document viewing closes with Esc. In the native client, using the first aid kit and opening F6/F7 were then checked.

## Devices and communication

Each instance gets its own ID, charge, OS, level and lock. The battery and power module restore charge, being consumed once. SIM is needed for telephone communication; number is associated with the instance. A regular laptop does not support changing the OS. Multi-loading is available on eligible models; the state OS additionally checks the real authorities in the registry. A phone with "Ghost OS" already contains this OS. Installed OSs are saved separately: switching through the device card consumes a unit of charge, but does not require a second flash drive and license. An ordinary laptop remains without multiboot.

SIM is consumed once during installation. “Basic” tariff: 300 ₽ for 7 game days, 20 calls and 100 messages; “Pro”: 900 ₽, 100 calls and 500 messages. These rates are added as build balance. Contacts are real phone numbers in NPC inventories nearby. A message of up to 140 characters is delivered to a specific phone at a distance of up to 150 m; histories are saved, 25 incoming and outgoing records each. A message costs 1 charge, a call costs 2; the recipient's phone consumes 1. The quota is debited only upon successful delivery. Some regular NPCs receive phones; There are no automatic replies or conversational AI.

The call is still a delivered event in history, without audio. News and radio use local magazine; There is no external network or multi-user voice communication. SDR scans real local telephones. Reading unencrypted history requires SChS, dossier access authority, radio 2, working SDR and 5 charges. "Ghost OS" hides the owner when scanning; Secure messages are not revealed by interception. The drone issues a local report within 100 m, without flight or video camera. The jammer suppresses local communications for 10 game minutes: standard - 50 m, makeshift - 15 m with a risk of breakdown of 50%. An active jammer is taken into account even after being thrown into the world. The staff model requires a government organization and Category A.

## Hacking

One job is performed at a time. The time below is game time. Necessary tools are checked at the beginning and at the end; consumables are written off upon successful creation of the result. The tools remain. Work, time, and risk rolls are preserved, so restarting does not recalculate the result. Failure locks the device for 24 in-game hours; hack PDA can also reduce its level. "Ghost OS" multiplies the risk of detection by 0.25. Detections are logged to the game system and are not hacks of actual devices.

| Operation | Time | Failure/Discovery | Tools | Materials | Skill |
|---|---:|---:|---|---|---|
| Hack PDA level 1 | 120 min | 10% / 5% | Programmer | — | technology 2 |
| Hack PDA level 2 | 240 min | 25% / 15% | JTAG adapter | — | technology 3 |
| Phone firmware | 60 min | 5% / 0% | Programmer | — | technology 2 |
| Installing a working OS | 30 min | 0% / 0% | Flash drive with OS | Basic working OS ×1 | — |
| Installing Ghost OS | 60 min | 10% / 0% | Flash drive with OS | Ghost OS ×1 | — |
| Installing the state OS | 30 min | 0% / 0% | Flash drive with OS | — | — |
| Card cloning | 20 min | 30% / 25% | Card reader | Blank Card ×1 | technology 1 |
| Signal interception | 360 min | 40% / 20% | SDR receiver | — | radio 2 |
| Device Audit | 60 min | 5% / 5% | Logic analyzer; JTAG adapter | — | technology 3 |
| USB embedding | 30 min | 15% / 10% | USB injector | — | — |

For the first hack you need PDA level 2, for the second - level 3. Card cloning is allowed for OCG or with “Technology 1”. USB injection is a criminal operation. A clone of a card does not open someone else's bank account: the withdrawal attempt is blocked and recorded. Signal interception works with available local targets, without an all-encompassing map network.

## Engineering segment

Practice improves skills: experience thresholds are 10 / 50 / 150. Courses cost 5,000 / 15,000 / 40,000 rubles. Profile organizations provide an effective level: engineering - Zonastroy and Chernenergo, technology - technology departments, radio communications - ComNet. Materials are consumed, tools are saved. A typical recipe lasts 30 in-game minutes.

| Result | Engineering Level | Tools | Consumables |
|---|---:|---|---|
| Device Battery | 1 | Set of screwdrivers and wrenches | Battery ×2; Copper wire (meter) ×1 |
| Power module | 3 | Soldering station; Multimeter; Drawings and electrical diagrams | Blank board ×1; Battery ×1; Copper wire (meter) ×1; Solder ×1; Flux ×1 |
| Armor repair kit | 2 | Welding machine; Welder mask | Steel sheet ×1; Electrodes ×1 |
| Homemade jammer | 3 | Soldering station; Drawings and electrical diagrams | Blank board ×1; Chips (set) ×1; Battery ×1; Solder ×1; Flux ×1 |
| Sharpening | 1 | File | Steel sheet ×1 |
| Electrical repair kit | 1 | Soldering iron; Multimeter | Blank board ×1; Copper wire (meter) ×1; Electrical tape ×1; Solder ×1; Flux ×1 |
| Mechanical repair kit | 1 | Set of screwdrivers and keys; Hacksaw | Steel sheet ×1; Electrical tape ×1 |
| Weapon repair kit | 2 | Set of screwdrivers and keys; File | Steel sheet ×1; Resistors and capacitors ×1 |
| Road sign STOP | 1 | Drill; Bulgarian; Set of screwdrivers and wrenches | Steel sheet ×1; Electrodes ×1 |
| USB media | 3 | Soldering station; Drawings and electrical diagrams | Blank board ×1; Chips (set) ×1; Solder ×1; Flux ×1 |

Diagnosing the device requires Engineering 1 and a multimeter. Engineering 2 with Oscilloscope covers more information about firmware, auditing, and implementation. Disassembling electronics requires engineering 1 and precision screwdrivers: the device is destroyed along with the SIM, installed OS and correspondence; It turns out a wire and a set of chips. Confirmation is required in the game menu, and not when preparing a modification. The stationary PC and defibrillator are not disassembled by this action.

The road sign MVD/IC is installed in the world and assembled back through the object card. The new simple STOP model is used on a stand with a base.

The electrical kit repairs electronics, the weapons kit repairs weapons; mechanical restores 25 percentage points of vehicle durability within 4 m. A destroyed vehicle is not restored. The armor boost is applied once and increases defense by 25% relative to the original, up to a maximum of 95%.

Workshop: live friendly mechanic or service station representative within 4 m; sewing_kit_b and money. Maintenance fully restores a weapon, armor or helmet and costs 30% of the base price of the item. For 15 new shooting models, real engine improvements are available: accuracy -20% for 10,000 ₽ and recoil -15% for 15,000 ₽; each adds 0.1 kg, is set once and saved. The game's standard weapon upgrades continue to apply.

## Licenses and medicine

| Document | Price | Who issues |
|---|---:|---|
| D | 5,000 ₽ | MVD, rank 1 |
| C | 15,000 ₽ | MVD, rank 1 |
| B | 50,000 ₽ | Ministry of Justice, rank 2 |
| A | 150,000 ₽ | MO, rank 2; certificate required IC |
| Certificate IC | free | IC, rank 2 |

The permit is tied to the owner, the physical copy, and the registry entry. The recipe additionally contains the drug, the number of doses and the duration: regular 7 days, narcotic 1 day, limited 3 days. Prescription drugs are tested for native use, not just on a menu button. Multi-dose packages and courses take into account actual doses and game days.

Automated specialists appear once at existing bases: MVD/MO - Cordon; Ministry of Justice, IC, doctor, pharmacist and M.O.P. - Bar; instructor and infectious disease specialist - Yantar; radiologist - Pripyat. They use existing buildings and NPC profiles. Five Bar specialists in the initial assembly were tested in the native client and after repeated loading; no other cards were visited in this check.

A field surgeon of the Ministry of Health has been added, including at the Bar base; a total of 11 service roles.

ARVI, pneumonia, food poisoning, three stages of radiation injury, chemical burn, bleeding, sepsis, spore infection, mutagenic injury and psi fever are simulated. Contact infection is checked within 3 m; raw food is different from cooked food. Radiation uses a normalized game scale, not physical millisieverts. Treatment is selected according to the specialist’s profile and disease; an inaccessible target is not replaced by the player.

The tourniquet stops bleeding and saves application time. After 180 game seconds, gangrene develops; requires treatment from a field surgeon. Removal before dressing may return the original bleeding. Duration - the accepted interpretation of the limitation specified in the source code; There is no separate model of tissue ischemia. Repeated native use of the tourniquet is blocked.

Defibrillator: 45,000 ₽, 2.2 kg, access to the Ministry of Health/MChS. Restores the health of a living critical NPC from ≤20% to 35% within 4 m; consumes 25 charges, break 120 game seconds. Dead NPCs do not resurrect. Price and parameters - balance of the assembly.

MChS-26G costs 35,000 ₽, weight 2.5 kg. Access: MChS, scientists, Alpha. Comes in a one-time package containing an antidote, a strong painkiller, burn gel, two bandages and adrenaline. Prescription drug restrictions remain. "+40% Survival" is not implemented as a permanent character bonus.

## Weapons, armor and evidence

The cartridges exist as real packs with the number of shots. Regular, Armor Piercing, Expansive, Rubber and Blank are available in major calibers; special calibers use separate types. Armor-piercing ones have a price multiplier of 1.6 and government access; expansive - 1.4 and criminal/contractual access. Rubber and blanks do not cause normal gunshot damage; rubber ones temporarily stun a valid NPC target. Stories and protected NPCs retain detention restrictions.

Protection is calculated separately for the head and body, taking into account the condition of the equipment. Booking types and required organizations are listed in the catalog below. Heavy kit prohibits sprinting. The front shield reduces hits in the ±60° sector by 60%, wears out; There is no separate hold animation yet. The stun gun works up to 4 m, gas - up to 3 m. The filter is valid for 60 game minutes only when wearing a working mask: GP-5 against chemistry, PMK against spores.

The photo/record preserves visible NPCs, position and weapons. To be added to the case, the recording must match the purpose and already registered violation at the time of filming. The mere snapshot of an armed NPC does not automatically create a new violation. Bank clone, detected transaction, and other events have separate journal entries. The log is limited to the last 100 entries.

The cooler container stores two source artifacts in a native hidden container. This is a transfer of the original objects, rather than the creation of copies: the identifier, state and properties of the study are preserved. The weight of the transported container takes into account the contents; the artifacts inside are not in the backpack and do not give the usual radiation from backpack items. The +20% bonus to the positive selling price of an artifact if there is a container is retained. A separate cooling model and power consumption are not yet available.

The visible weapon check takes into account the owner's valid physical license and registry entry. MVD/IC with the power of observation, register a case under the missing category D/C/B: a fine of 20,000 rubles through the usual procedural chain. Category A maps to existing entry `uk_11_2`; the new independent criminal term from the PDF has not been added. The check concerns weapons in hands, not hidden equipment; The button itself does not write off the fine and does not replace the judicial procedure.

## Transport

These are real ground CCar objects with engine, tank, physics and state saving. Motor values ​​are taken from current configurations; New prices are assigned for this build and are not the prices of missing vehicles from the PDF.

| Machine | Purchase | Rent / day | Tank, l | Power in config | X-Ray Consumption | Section/spawn |
|---|---:|---:|---:|---:|---:|---|
| Mercedes-Benz S-Class W140 | 500000 ₽ | 20000 ₽ | 100 | 408 | 6.5 | `cczmp_veh_w140` |
| Niva - standard X-Ray model | 120000 ₽ | 6000 ₽ | 45 | 80 | 2.3 | `cczmp_veh_niva` |
| UAZ-469 - standard X-Ray model | 180000 ₽ | 9000 ₽ | 78 | 75 | 2.6 | `cczmp_veh_uaz469` |
| UAZ Bukhanka | official issue | — | 80 | 65 | 2.6 | `cczmp_veh_buhanka` |
| KAMAZ - standard X-Ray model | official issue | — | 250 | 150 | 8 | `cczmp_veh_kamaz` |
| BTR-80 | official issue | — | 250 | 260 | 6 | `cczmp_veh_btr` |

X-Ray consumption is specified in liters per 100,000 engine revolutions, and not in l/100 km. Strength is normalized from 0 to 1; the new car has 1. The maximum speed has not been measured experimentally. In the native test, the Niva independently drove 27.09 m under the influence of the engine; This is a motion test, not a speed measurement.

Purchase and rental are processed by a M.O.P. specialist. within 4 m. The rental lasts 86,400 game seconds, extension adds a day. After the deadline has expired, the engine stops; the occupied vehicle is not deleted. Return - from a specialist, the car is no further than 8 m, the player is outside the cabin. The gas station sells up to 20 liters at 100 ₽/l, the actual fuel placed is paid for; need a car up to 8 m and a trader/M.O.P. up to 4 m.

The issuance of a company car requires the appropriate organization and its own maximum rank or a friendly boss of the same organization within 4 m. Loaf: court, MVD, OMON, FSIN, Ministry of Health, Ministry of Justice, MChS/SChS. KAMAZ: “Zonastroy”, “Chernenergo”, Ministry of Energy, Moscow Region. BTR: MO, BBN. In debugging, output restrictions are dealt with in a separate mode.

Spawn is looking for a free, flat area, checking navmesh, dimensions, NPCs and other vehicles. In cramped spaces, dispensing may be rejected; in an open place, a car can appear at a distance of up to 56 m. The car and PC cannot be put into inventory.

GPS is installed by M.O.P./car mechanic within 4 m for 6,000 ₽; engine blocking - 8,000 ₽. The car must belong to the player, be nearby, be in good working order and parked with the engine turned off. Rented cars are not equipped. GPS tags a real car and is suppressed by a local jammer. The lock keeps the engine off and applies the handbrake; She doesn’t lock the doors or boarding, and there’s no siren yet. The setting and status are saved. These prices are the balance of the build; The service station "Kaban" is not used as a car service.

Source reference cards are available in the general transport catalog. You can buy or create through F7 only six machines with installed native resources; Inaccessible cards do not debit money. For the Ka-226, L-410 and EC135, the initial tank, speed and flow rate are shown, which are not yet the physical characteristics of the controlled equipment.

## Remaining and visual prototypes

- New devices use simple native prototype models. For exact models of each brand, new hands/animations and shields, separate work with assets is required.
- LC100, Jeep, Patrol, Patriot, Expedition, Geländewagen, X5, Range Rover, Ka-226, L-410 and EC135 from PDF were not replaced by Niva or W140. Their new full-fledged models and player-controlled aircraft are missing. UAZ-469 is not called Patriot.
- Concrete mixer, excavator, crane, new physical real estate buildings, doors and full-fledged construction equipment have not been implemented.
- There is no multi-stage car tuning with speed bonuses, a new system of passenger seats/crew transportation and drone flight.
- All PDF legal rules are not yet covered: visible weapon checks and procedural fines are added, but new automatic inventory searches, stand-alone new criminal sentences and a full block of crimes with prescriptions are missing.
- Coded master keys, automatic placement of signs on maps, flashing lights and physical additional seats are not yet available. Tariffs, defibrillator, surgeon, portable sign and gangrene are implemented in the scope described above.
- MSG-V1/Teg-9 use game prototypes on existing weapon models. SV-98 with the .338 cartridge is a conventional CCZMP configuration on the native 7.62 base, not an exact match to the real weapon. The judge's robe and robe are also visual prototypes for now.
- Radio, media and container are implemented in the scope described above; full voice communication, drone flight/camera, physical construction equipment, and new building models remain separate tasks.

## Installation and rollback

On the working device, changes have already been made to `D:\\CCZMP PROJECT`. The archive is an addition to this version of CCZMP, and not a complete clean build of Anomaly. Close the game, make a copy of the project, transfer `gamedata` from the archive with a directory merge; `tools/tests` contains updated checks. User saves are not included in the archive.

Backup before changes: `D:\\CCZMP PROJECT\\_backups\\items_hacking_20261009_074317`. To rollback, restore files marked as existing in the manifest from this copy; delete only files with `new: true`. Before rolling back, save new game saves separately: they may contain new sections of items and equipment.

Backup before continuing: `D:\\CCZMP PROJECT\\_backups\\items_continuation_20261009_124604`; in its manifest `old: null` means new file. Restoring this copy returns the previous stage rather than a clean Anomaly.

## Checks

128 legacy regression checks, 51 initial segment checks, and 21 additional continuation checks—200 checks. Natively tested communications, multi-boot, defibrillator, tourniquet, engineering actions, original artifacts in container, GPS/engine lock and repeat loading. After the message form, F6/F7 opened. Details and limits of verification - `verification/continuation_review.md`. The container was not transferred natively between locations; the open area for visual assessment of the new sign model has not been tested.  Native client: items and packs of ammo, recipes/licenses, use of medicines, saving an active operation, cold loading, unpacking the MChS set, two AKM upgrades, five Bar specialists, engines and physics of five new cars, Niva repair/tank and real movement. After viewing the passport, Esc, F6, F7 and the use of the item were checked. These are functional checks; Long-term game balance and completion of all locations have not yet been tested.

## Full catalog

Price—the nominal price of the catalog in rubles; weight - kg. Organizations are listed by internal identifiers for precise configuration searching. Access to medications and documents is additionally determined by the rules above. `—` means there is no additional metadata requirement.

### PDA

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| PDA basic | 8000 | 0.2 | — | `device_pda_1` |
| PDA 2 - hacking | 35000 | 0.25 | — | `device_pda_2` |
| PDA 3 - hacking | 90000 | 0.3 | — | `device_pda_3` |
| PDA specialist | 55000 | 0.4 | — | `cczmp_kpk_hacker` |
| Specialist tablet | 120000 | 0.8 | — | `cczmp_tablet_hacker` |

### PDA

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| PDA-bulletin | 2000 | 0.25 | — | `cczmp_kpk_bulletin` |

### Laptops

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| Basic laptop | 60000 | 2.4 | — | `cczmp_laptop_basic` |
| Multiboot Laptop | 150000 | 2.8 | — | `cczmp_laptop_multi` |
| Specialist laptop | 190000 | 3.1 | — | `cczmp_laptop_hacker` |

### Desktop PC

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| PC desktop | 120000 | 12 | — | `cczmp_pc_desktop` |

### Phones

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| Regular phone | 15000 | 0.18 | — | `cczmp_phone_basic` |
| Protected phone | 70000 | 0.2 | — | `cczmp_phone_secure` |
| Phone with Ghost OS | 95000 | 0.22 | — | `cczmp_phone_hacker` |

### Tablet

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| Civil tablet | 35000 | 0.65 | — | `cczmp_tablet_basic` |

### supply

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| SIM module | 3000 | 0.01 | — | `cczmp_sim_module` |
| Flash drive with OS | 5000 | 0.02 | — | `cczmp_usb_os` |
| Ghost OS | 20000 | 0.01 | — | `cczmp_os_ghost` |
| Basic working OS | 5000 | 0.01 | — | `cczmp_os_linux` |
| Device Battery | 1500 | 0.08 | — | `cczmp_battery_device` |
| NBZ bank card | 3000 | 0.01 | — | `cczmp_bank_card` |
| Blank card | 1000 | 0.01 | — | `cczmp_blank_card` |
| Cloned card | 0 | 0.01 | — | `cczmp_cloned_card` |

### tool

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| Jewelry screwdrivers | 800 | 0.2 | — | `cczmp_precision_screwdrivers` |
| Programmer | 25000 | 0.4 | — | `cczmp_programmer` |
| JTAG adapter | 40000 | 0.15 | — | `cczmp_jtag` |
| Card reader | 12000 | 0.15 | — | `cczmp_card_reader` |
| Logic Analyzer | 60000 | 0.3 | — | `cczmp_logic_analyzer` |
| SDR receiver | 35000 | 0.25 | — | `cczmp_sdr` |
| Local jammer | 70000 | 1.2 | — | `cczmp_jammer` |
| USB injector | 15000 | 0.04 | — | `cczmp_usb_injector` |
| Soldering iron | 1500 | 0.3 | — | `cczmp_soldering_iron` |
| Multimeter | 2500 | 0.3 | — | `cczmp_multimeter` |
| Oscilloscope | 40000 | 4 | — | `cczmp_oscilloscope` |
| Soldering station | 18000 | 2 | — | `cczmp_soldering_station` |
| Welding machine | 25000 | 5 | — | `cczmp_welder` |
| Welder mask | 2000 | 0.6 | — | `cczmp_welding_mask` |
| Hacksaw | 1200 | 0.6 | — | `cczmp_hacksaw` |
| File | 600 | 0.4 | — | `cczmp_file` |
| Drill | 5000 | 1.8 | — | `cczmp_drill` |
| Bulgarian | 8000 | 2.2 | — | `cczmp_grinder` |
| Set of screwdrivers and wrenches | 3000 | 1.6 | — | `cczmp_toolset` |

### material

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| Solder | 300 | 0.1 | — | `cczmp_solder` |
| Flux | 200 | 0.1 | — | `cczmp_flux` |
| Electrodes | 400 | 0.5 | — | `cczmp_electrodes` |
| Copper wire (meter) | 50 | 0.05 | — | `cczmp_copper_wire` |
| Blank board | 400 | 0.03 | — | `cczmp_blank_board` |
| Resistors and capacitors | 800 | 0.08 | — | `cczmp_components` |
| Chips (set) | 3000 | 0.06 | — | `cczmp_chips` |
| Battery | 1500 | 0.05 | — | `cczmp_cell` |
| Sheet steel | 2000 | 1 | — | `cczmp_steel_sheet` |
| Electrical tape | 150 | 0.04 | — | `cczmp_electrical_tape` |

### equipment

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| Power module | 6500 | 0.25 | — | `cczmp_power_module` |
| Drawings and electrical diagrams | 2500 | 0.1 | — | `cczmp_blueprint` |
| Armor repair kit | 8000 | 1.2 | — | `cczmp_repair_armor` |
| Weapon repair kit | 10000 | 0.8 | — | `cczmp_repair_weapon` |
| Electrical repair kit | 4500 | 0.4 | — | `cczmp_repair_device` |
| Mechanical repair kit | 6000 | 1 | — | `cczmp_repair_mechanical` |
| Homemade jammer | 15000 | 0.5 | — | `cczmp_jammer_makeshift` |
| Megaphone | 1500 | 0.7 | — | `cczmp_megaphone` |
| Walkie-talkie "Volna-M" | 8000 | 0.35 | — | `cczmp_radio` |
| DVR 360 | 12000 | 0.3 | — | `cczmp_dashcam` |
| Media set “Voice of the Law” | 12000 | 1.5 | — | `cczmp_media_kit` |
| Gas mask filter | 3000 | 0.3 | — | `cczmp_filter` |
| Teiser | 12000 | 0.5 | D/mvd,fsin | `cczmp_taser` |
| Gas cartridge | 1500 | 0.5 | — | `cczmp_spray` |
| Service shield | 25000 | 2 | omon,fsin | `cczmp_shield` |
| Artifact Cooler Container | 70000 | 0.5 | — | `cczmp_cooler` |
| Defibrillator | 45000 | 2.2 | minzdrav,mchs | `cczmp_defibrillator` |
| Road sign STOP (set) | 5000 | 4 | mvd,sk | `cczmp_road_sign` |
| Oko reconnaissance drone | 80000 | 0.5 | — | `cczmp_drone` |

### Weapons

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| Sharpening | 1000 | 0.25 | — | `cczmp_shank` |
| PM with silencer | 18000 | 0.73 | D | `wpn_cczmp_pm` |
| USP Match 9x19 with suppressor | 45000 | 0.88 | D | `wpn_cczmp_usp` |
| MP-7 / 4.6×30 | 85000 | 1.9 | C | `wpn_cczmp_mp7` |
| Teg 9 - prototype | 110000 | 2.1 | C | `wpn_cczmp_teg9` |
| MSG-V1 - prototype | 70000 | 3.4 | C | `wpn_cczmp_msgv1` |
| M-16 CCZMP | 60000 | 3.4 | B | `wpn_cczmp_m16` |
| Administrative Code-74 CCZMP | 40000 | 3.3 | B | `wpn_cczmp_ak74` |
| AKM CCZMP | 25000 | 3.5 | B | `wpn_cczmp_akm` |
| HK416 CCZMP | 180000 | 3.5 | B | `wpn_cczmp_hk416` |
| SVD CCZMP | 95000 | 4.3 | B | `wpn_cczmp_svd` |
| SV-98 CCZMP/.338 | 350000 | 6.2 | A | `wpn_cczmp_sv98` |
| Saiga-12 CCZMP | 35000 | 3.6 | B | `wpn_cczmp_saiga` |
| Vepr-12 CCZMP | 60000 | 4.3 | B | `wpn_cczmp_vepr` |
| PCM CCZMP | 220000 | 7.5 | A | `wpn_cczmp_pkm` |
| RPG-7 CCZMP | 150000 | 6.3 | A | `wpn_cczmp_rpg` |
| Knife CCZMP | 800 | 0.2 | — | `wpn_cczmp_knife` |

### document

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| Weapons license category D | 5000 | 0.02 | — | `cczmp_license_d` |
| Weapons license category C | 15000 | 0.02 | — | `cczmp_license_c` |
| Category B Weapons License | 50000 | 0.02 | — | `cczmp_license_b` |
| Category A Weapons License | 150000 | 0.02 | — | `cczmp_license_a` |
| Help IC for category A | 0 | 0.02 | — | `cczmp_sk_certificate` |
| Personalized medical prescription | 0 | 0.02 | — | `cczmp_prescription` |

### Medicines

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| CCZMP Bandage | 300 | 0.08 | — | `cczmp_med_bandage` |
| CCZMP Harness | 800 | 0.08 | — | `cczmp_med_tourniquet` |
| Small first aid kit | 2500 | 0.08 | — | `cczmp_med_medkit_small` |
| CCZMP First Aid Kit | 5000 | 0.08 | — | `cczmp_med_medkit` |
| Broad spectrum antibiotic | 4000 | 0.08 | — | `cczmp_med_antibiotic` |
| Antipyretic | 300 | 0.08 | — | `cczmp_med_antipyretic` |
| Pain reliever | 1200 | 0.08 | — | `cczmp_med_painkiller` |
| Powerful pain reliever | 3500 | 0.08 | — | `cczmp_med_strong_painkiller` |
| Antirad CCZMP | 6000 | 0.08 | — | `cczmp_med_antirad` |
| Iodine tablets | 1500 | 0.08 | — | `cczmp_med_iodine` |
| Universal antidote | 9000 | 0.08 | — | `cczmp_med_antidote` |
| Adrenaline CCZMP | 5000 | 0.08 | — | `cczmp_med_adrenaline` |
| Anti-strain serum | 25000 | 0.08 | — | `cczmp_med_serum` |
| Immunomodulator | 8000 | 0.08 | — | `cczmp_med_immunomodulator` |
| CCZMP Psi Blocker | 15000 | 0.08 | — | `cczmp_med_psiblocker` |
| Regidron | 1500 | 0.08 | — | `cczmp_med_rehydration` |
| Remedy for chemical burns | 2500 | 0.08 | — | `cczmp_med_burn_gel` |

### Ammunition

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| 9x18 - regular | 1200 | 0.2 | — | `cczmp_ammo_9x18_fmj` |
| 9x18 - armor-piercing | 1920 | 0.2 | state | `cczmp_ammo_9x18_ap` |
| 9x18 - expansive | 1680 | 0.2 | criminal contract | `cczmp_ammo_9x18_hp` |
| 9x18 - rubber | 1200 | 0.2 | mvd,omon,fsin,minjust | `cczmp_ammo_9x18_rubber` |
| 9x18 - single | 300 | 0.2 | — | `cczmp_ammo_9x18_blank` |
| 9x19 - regular | 1800 | 0.6 | — | `cczmp_ammo_9x19_fmj` |
| 9x19 - armor-piercing | 2880 | 0.6 | state | `cczmp_ammo_9x19_ap` |
| 9x19 - expansive | 2520 | 0.6 | criminal contract | `cczmp_ammo_9x19_hp` |
| 9x19 - rubber | 1800 | 0.6 | mvd,omon,fsin,minjust | `cczmp_ammo_9x19_rubber` |
| 9x19 - single | 300 | 0.4 | — | `cczmp_ammo_9x19_blank` |
| 5.45x39 - regular | 2400 | 0.33 | — | `cczmp_ammo_545_fmj` |
| 5.45x39 - armor-piercing | 3840 | 0.33 | state | `cczmp_ammo_545_ap` |
| 5.45×39 - expansive | 3360 | 0.33 | criminal contract | `cczmp_ammo_545_hp` |
| 5.45×39 - rubber | 2400 | 0.33 | mvd,omon,fsin,minjust | `cczmp_ammo_545_rubber` |
| 5.45×39 - single | 300 | 0.22 | — | `cczmp_ammo_545_blank` |
| 7.62x39 - regular | 2000 | 0.48 | — | `cczmp_ammo_76239_fmj` |
| 7.62×39 - armor-piercing | 3200 | 0.48 | state | `cczmp_ammo_76239_ap` |
| 7.62×39 - expansive | 2800 | 0.48 | criminal contract | `cczmp_ammo_76239_hp` |
| 7.62×39 - rubber | 2000 | 0.48 | mvd,omon,fsin,minjust | `cczmp_ammo_76239_rubber` |
| 7.62×39 - blanks | 300 | 0.32 | — | `cczmp_ammo_76239_blank` |
| 5.56x45 - regular | 2800 | 0.36 | C | `cczmp_ammo_556_fmj` |
| 5.56×45 - armor-piercing | 4480 | 0.36 | C/state | `cczmp_ammo_556_ap` |
| 5.56×45 - expansive | 3920 | 0.36 | C/criminal,contract | `cczmp_ammo_556_hp` |
| 5.56×45 - rubber | 2800 | 0.36 | C/mvd,omon,fsin,minjust | `cczmp_ammo_556_rubber` |
| 5.56×45 - single | 300 | 0.24 | C | `cczmp_ammo_556_blank` |
| 7.62×54R - regular | 3200 | 0.48 | B | `cczmp_ammo_76254_fmj` |
| 7.62×54R - armor-piercing | 5120 | 0.48 | B/state | `cczmp_ammo_76254_ap` |
| 7.62×54R - expansive | 4480 | 0.48 | B/criminal,contract | `cczmp_ammo_76254_hp` |
| 7.62×54R - rubber | 3200 | 0.48 | B/mvd,omon,fsin,minjust | `cczmp_ammo_76254_rubber` |
| 7.62×54R - idle | 300 | 0.48 | B | `cczmp_ammo_76254_blank` |
| 12/70 fraction - regular | 900 | 0.4 | B | `cczmp_ammo_12shot_fmj` |
| 12/70 shot - armor-piercing | 1440 | 0.4 | B/state | `cczmp_ammo_12shot_ap` |
| 12/70 shot - expansive | 1260 | 0.4 | B/criminal,contract | `cczmp_ammo_12shot_hp` |
| 12/70 shot - rubber | 900 | 0.4 | B/mvd,omon,fsin,minjust | `cczmp_ammo_12shot_rubber` |
| 12/70 fraction - blanks | 300 | 0.8 | B | `cczmp_ammo_12shot_blank` |
| 12/70 buckshot - regular | 1500 | 0.225 | B | `cczmp_ammo_12buck_fmj` |
| 12/70 buckshot - armor-piercing | 2400 | 0.225 | B/state | `cczmp_ammo_12buck_ap` |
| 12/70 buckshot - expansive | 2100 | 0.225 | B/criminal,contract | `cczmp_ammo_12buck_hp` |
| 12/70 buckshot - rubber | 1500 | 0.225 | B/mvd,omon,fsin,minjust | `cczmp_ammo_12buck_rubber` |
| 12/70 buckshot - blanks | 300 | 0.9 | B | `cczmp_ammo_12buck_blank` |
| .338 Lapua CCZMP - regular | 6000 | 0.45 | A | `cczmp_ammo_338_fmj` |
| .338 Lapua CCZMP - armor-piercing | 9600 | 0.45 | A/state | `cczmp_ammo_338_ap` |
| .338 Lapua CCZMP - Expansive | 8400 | 0.45 | A/criminal,contract | `cczmp_ammo_338_hp` |
| .338 Lapua CCZMP - rubber | 6000 | 0.45 | A/mvd,omon,fsin,minjust | `cczmp_ammo_338_rubber` |
| .338 Lapua CCZMP - blanks | 300 | 0.9 | A | `cczmp_ammo_338_blank` |
| 12.7x108 - regular | 9000 | 1.25 | A/state | `cczmp_ammo_127_fmj` |
| VOG-25 - conventional | 4500 | 1.25 | A | `cczmp_ammo_vog_fmj` |
| VOG-25 fragmentation - conventional | 7000 | 0.75 | A/state | `cczmp_ammo_vog_state_fmj` |
| 4.6x30 - regular | 3000 | 0.18 | C | `cczmp_ammo_4630_fmj` |
| 4.6×30 - armor-piercing | 4800 | 0.18 | C/state | `cczmp_ammo_4630_ap` |
| 4.6x30 - expansive | 4200 | 0.18 | C/criminal,contract | `cczmp_ammo_4630_hp` |
| 4.6×30 - rubber | 3000 | 0.18 | C/mvd,omon,fsin,minjust | `cczmp_ammo_4630_rubber` |
| 4.6×30 - single | 300 | 0.12 | C | `cczmp_ammo_4630_blank` |
| OG-7V for RPG-7 - regular | 9000 | 2 | A | `cczmp_ammo_rpg_fmj` |

### armor

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| Light vest | 8000 | 3 | — | `cczmp_armor_light` |
| Patrol vest MVD | 25000 | 5 | mvd | `cczmp_armor_patrol` |
| Plate carrier Alpha | 90000 | 8 | alfa,vympel | `cczmp_armor_plate` |
| Heavy vest OMON | 150000 | 14 | omon | `cczmp_armor_omon` |
| Heavy Armor Suit | 320000 | 22 | mo,bbn | `cczmp_armor_heavy` |
| Service vest IC | 20000 | 3 | sk | `cczmp_armor_sk` |
| Hidden Vest | 35000 | 1.5 | criminal,business | `cczmp_armor_hidden` |
| Urban jacket | 2000 | 4 | — | `cczmp_clothes_city` |
| Field suit | 4000 | 4 | criminal | `cczmp_clothes_field` |
| Judge's robe - prototype | 15000 | 4 | sud,minjust | `cczmp_clothes_judge` |
| Scientist's robe - prototype | 12000 | 4 | scientists,mintechnology | `cczmp_clothes_scientist` |
| Germo protective suit | 150000 | 4 | ob_cheg,scientists | `cczmp_clothes_hermo` |

### Helmets

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| Construction helmet | 2000 | 1.2 | zonastroy, chernenergo | `cczmp_helmet_construction` |
| Rescue helmet | 9000 | 1.2 | mchs | `cczmp_helmet_rescue` |
| Tactical helmet | 45000 | 1.2 | omon,alfa | `cczmp_helmet_tactical` |
| Ballistic helmet with visor | 120000 | 1.2 | omon,alfa | `cczmp_helmet_visor` |
| Helmet with headset | 60000 | 1.2 | alfa,vympel | `cczmp_helmet_headset` |
| Gas mask GP-5 | 25000 | 1.2 | — | `cczmp_helmet_gp5` |
| Gas mask PMK | 60000 | 1.2 | — | `cczmp_helmet_pmk` |

### kit

| Subject | Price, ₽ | Weight, kg | License/Organization | Section for F7 |
|---|---:|---:|---|---|
| First aid kit "Spetsnaz-MChS" / 26G | 35000 | 2.5 | mchs,scientists,alfa | `cczmp_medkit_mchs` |
