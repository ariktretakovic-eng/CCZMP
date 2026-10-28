[Русский](../../../snapshot-2026-10-28/CCZMP_DONOR_COMPLETION_2026-10-18.md) · **English** · [Documentation index](../INDEX.md) · [Translation notes](../../TRANSLATION.md)

# CCZMP - transfer of remaining donors, October 18, 2026

Working build: Anomaly 1.5.1. The package is installed directly into gamedata.
Backup: D:\CCZMP PROJECT\_backups\donor_completion_20261018_202533
Recovery: C:\Python314\python.exe tools\donor_completion_20261018\rollback.py.
Rollback first checks the hashes: it does not overwrite other people's changes. The player's saves and settings are not restored or deleted.

## What's added

All 12 archives not matched to the previous transfer have been processed: eight cars, operator SChS, two Valorant weapons and a police set of eight individual items. Four existing inventory drones received physical flying versions. A total of 25 new OGF and 336 installed files with textures, configs and scripts.

| Section | Model | Weight, kg | Power, gaming parameter | Tank, l |
|---|---|---:|---:|---:|
| cczmp_fv_203 | Lada Priora | 1260 | 98 | 43 |
| cczmp_fv_204 | GAZ-3221 Gazelle | 2800 | 120 | 70 |
| cczmp_fv_205 | GAZelle NEXT | 3000 | 150 | 80 |
| cczmp_fv_206 | GAZelle NEXT - ambulance | 3500 | 150 | 80 |
| cczmp_fv_207 | MAZ-7310 Prototype | 28000 | 525 | 500 |
| cczmp_fv_208 | MAZ-6440RR Dakar MChS | 9500 | 600 | 250 |
| cczmp_fv_209 | GAZ-233036 Tiger OMON | 7200 | 205 | 140 |
| cczmp_fv_210 | Paddy wagon FSIN - restored | 7000 | 150 | 120 |

The parameters serve as game settings, and not as passport specifications. The MAZ-7310 has eight physical wheels, the paddy wagon has six; the rest are four. The cars have separate points for wheels, landing, camera and lights, transparent windows, inheritance of the current fuel system, trunk and damage. An entire car has been isolated from the paddy wagon scene and debris and dirt have been removed. The extraneous human figure has been removed from Gazelle. W140_SK and older transport models were not replaced.

Civilian vehicles have been added to the transport catalogue: Priora - 180,000, Gazelle - 380,000; service ones are available through issuing your organization and debugging. Access is verified by the existing system of organizations. Empty access fields have been fixed: an empty value means no restriction, as provided by the config. Company car sirens use organizational profiles.

## How to get

F7 → CCZMP donor catalog:
- “New transport: civil and official” - sections 203–210.
- “SChS NChG” - operator 211.
- “Additional weapons” - Operator 212, Vandal 213.
- “Road equipment MVD” - items 214–221.
- Drones - existing items 042–045 in the item/donor catalog.

Regular purchases and service pickup use existing CCZMP menus from merchants; Availability on menu depends on organization access. There was no verification of actual payment from each individual merchant in this package.

## Drones

| Subject | Flying section | Model | Speed, m/s | Height limit, m | Communication, m | Explosion radius, m |
|---|---|---|---:|---:|---:|---:|
| cczmp_fitem_042 | cczmp_fa_042 | DJI FPV | 16 | 100 | 300 | 4 |
| cczmp_fitem_043 | cczmp_fa_043 | Shahed 136 option 1 | 28 | 160 | 650 | 12 |
| cczmp_fitem_044 | cczmp_fa_044 | Shahed-107 | 24 | 140 | 500 | 9 |
| cczmp_fitem_045 | cczmp_fa_045 | Shahed-136, option 2 | 28 | 160 | 650 | 12 |

In the item properties, select “Launch and connect to the drone.” Requires free space and charge. The inventory item is consumed only after the appearance of a working physical device. The operator remains on the ground; Drone landing is prohibited. The camera remains with the operator; there is no separate FPV video channel.

Controls: W/S - forward/backward, A/D - sideways, Q/E - turn, PgUp/PgDn - height, Space - hover, R - reconnaissance, Esc - turn off.
Intelligence records visible living NPCs within 100m with static obstacle checks. The result is available through “My drones” → reconnaissance.

“My Drones” in the item menu allows you to connect again and pick up the device. For collection: distance up to 5 m, height up to 1.4 m, speed less than 1.42 m/s. The original item type, UID, and remaining charge are returned. Loss of communication, interference or Esc puts the device into hold position; when discharged, the engine stops.

Contact after takeoff causes a one-time destruction and logging. The body, chassis and the distance traveled between frames are checked. Before lifting off from the launch site, the inspection is not armed. A small tolerance at ground covers the contact of the physical chassis. Helicopter fragments are disabled: the defeat sets the script with a separate radius for each profile.

Charge consumption: DJI 0.12%/s, 043/045 - 0.08%/s, 044 - 0.10%/s. This is the balance of the current implementation. All devices use a common stabilized flight controller; There is no own aerodynamics of the aircraft wing and no unique animations of the propellers.

## Organizations and weapons

cczmp_fnpc_211 — operator SChS, visual actors\cczmp\donors\cczmp_fn_211.ogf.
Moved from the Mixamo skeleton to the regular stalker skeleton, tied to agency_schs. Uses standard movements and AI. Other organizational appointments have been retained.

wpn_cczmp_fd_212 — Operator, game base SV-98, magazine 5, single fire, ammo_7.62x54_7h1.
wpn_cczmp_fd_213 - Vandal, AKM game base, 30 magazine, single/automatic fire, ammo_7.62x39_fmj.
HUD and world models have been transferred; Standard shooting/reloading/aiming mechanics are used. No new hand animations were created.

## Road equipment

| Index | Subject | Action |
|---|---|---|
| 214 | Traffic cone | Installation/assembly, moving physical object |
| 215 | Tripod Radar | Automatic speed measurement |
| 216 | Mobile DPS shield | Installation/assembly, physical obstacle |
| 217 | Round sign | Installation/Assembly |
| 218 | Information board | Installation/Assembly |
| 219 | Oval sign | Installation/Assembly |
| 220 | Emergency triangle | Installation/Assembly |
| 221 | Triangular sign | Installation/Assembly |

Inventory sections cczmp_fitem_214..221, world sections cczmp_fworld_214..221. The size of the emergency triangle is 45 cm, the cone is 70 cm; signs about 2 m. Access MVD/IC is inherited from road equipment. Install from the properties of the item, pick up along F within 3 m. The owner or an employee of the same organization can pick up; requesting again does not create a second item.

The radar checks vehicles every 0.5 s: up to 80 m, sector 120 degrees, height difference up to 5 m, line of sight. Aircraft are excluded. The speed is taken from the physical shell and converted to km/h; per machine no more than once every 5 seconds. The log stores the last 100 measurements with the car, operator, device, location and game time. View - "Road Radar Measurements". Automatic fines and legal qualifications are not connected to the measurements. The radar's charge is consumed during operation and stored during collection.

## Checks and materials

driving tests eight vehicles, real shooting of both weapons, spawn and NPC model, installation of eight road items made in real AnomalyDX9AVX.
Fixtures and results: tools\donor_completion_20261018\native_*.json, native_live*.log and snapshots *.jpg.
Verification of resources: asset_verification.json - 25 OGF, no missing textures, 200 comparisons of the previous Mi-2 mathematics without changing the result.
47 original user save/settings files are hash checked after each installation; tests are carried out in a separate profile native_appdata.

## Carry boundaries

This is not a rewrite of the engine. Old truck cranes, forestry equipment, Tor-M1, railway transport, Rafale and flying motorcycle retain the pre-existing prototype status of special mechanisms. The operation of the boom, a full-fledged Tor air defense system/radar, movement strictly on rails and the aerodynamics of the Rafale are not added by this package. 11 disabled cards without original models were not turned on artificially.

The source archives and their attribution/license files are left in tools\donors and prepared sources/extra. The publicity rights of each third party donor have not been verified.
