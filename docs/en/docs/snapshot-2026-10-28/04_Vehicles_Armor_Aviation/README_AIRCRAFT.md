[Русский](../../../../snapshot-2026-10-28/04_%D0%A2%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82_%D0%B1%D1%80%D0%BE%D0%BD%D0%B5%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0_%D0%B0%D0%B2%D0%B8%D0%B0%D1%86%D0%B8%D1%8F/README_AIRCRAFT.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# STALKER x CCZMP - Mi-2, free flight prototype

Prototype for the current build of Anomaly 1.5.1 build8028. Uses the standard external Mi-2 model with a redesigned physical skeleton and its own CCZMP controller. EXE substitution is not required. This is an addition to the existing CCZMP build, not a standalone addon for pure Anomaly.

## Creation and management

On an open, flat area, open F7, action tab, and select “Mi-2: create flight prototype.” Also Mi-2 is in the transport catalogue. Debug must be enabled. If there is no suitable site, creation is canceled with the message: move to a freer site.

| Key | Action |
|---|---|
| F at the left or right side of the cabin | Sit in the cockpit |
| J | Start/stop engine |
| Page Up / Page Down | Rise/decline |
| W/S | Forward/backward movement |
| A/D | Lateral movement |
| Q/E | Rotate |
| Space | Braking and maintaining current altitude |
| X | Exit after stopping, landing and stopping the propeller |

To land, go to the side of the cabin, aim at the body, press and release F.

After starting, wait for the screw to spin - about 5 seconds. When you release the movement keys, the controller slows down the helicopter; When you release the rise/decrease, it remembers the current altitude. Turning off the engine removes thrust as the propeller stops, so the engine should not be turned off while in the air.

The panel shows the engine status, propeller spin, fuel reserve, horizontal speed, vertical speed and altitude relative to the creation site. The last value **is not the height above the current terrain**.

## Prototype parameters

| Parameter | Meaning |
|---|---|
| Physical body mass | 2800 kg |
| Fuel tank | 600 l |
| Operating engine consumption | 120 l/hour of game update, without taking into account the calendar time scale |
| Target forward speed | 30 m/s, 108 km/h |
| Target Lateral Speed ​​| 15 m/s, 54 km/h |
| Rise/decline | 4 / 2 m/s |
| Height limit | 200 m relative to the place of creation |
| Unwinding/stopping the propeller | Approximately 5 / 8.3 seconds |

Speeds are controller settings, not guaranteed performance characteristics of the real Mi-2. The flight model is simplified, with automatic stabilization. For the current CCar, the controller takes into account half of the world's gravity compensation and a physical step of 10 ms. When replacing the engine, a re-check is required.

Fuel is preserved by the existing transport system; the state of the engine, propeller and altitude held are stored in the ALife storage of a specific instance. The position and physical condition are preserved by the engine. The radio and service use a common CCZMP transport binder. The car trunk is excluded for the Mi-2, so that the F at the tail does not open the car cargo interface.

## Boundaries of the current version

One pilot; stock outer hull instead of new detailed cockpit. The tail rotor does not yet have a separate animation. Blade collision simplified. Weapons, passengers, route autopilot, NPC air patrols, flights between levels and network synchronization are not included in this prototype. Purchasing from a merchant is not yet configured; creation is available via debug.

## Checks

Landing is verified by a real F event (press and release), with the CCar owner, player position, and camera checked. Unit checks cover deferred use, F hold, expired requests, ID reuse, and byte-by-byte retention of the old physical package when adding entry points.

Native test results are in `verification/`. In the real F landing run, pilot anchoring, camera following, takeoff at 18.90 m, hover at 19.08 m, forward movement at 6.85 m, braking and turning were confirmed. Tested controller math constraints and Lua 5.1 syntax. A separate loading mid-air save confirmed the restoration of the pilot, camera, fuel, engine and altitude held. Checked the radio, returning control after closing its window, landing, stopping the engine, exiting and re-creating via F7. The format of the old Mi-2 with zero entry points is tested through a real server package and the re-creation of the physical body: ID and name are saved, position deviation is 0.041 m, the fuel difference corresponds to the engine consumption. Native testing is performed on DX9 AVX; other renderers have not been tested separately.

Challenges use separate copies of saves. User settings are restored byte by byte; checksums of user saves are compared before and after each run.

## Files and rollback

The installation has already been completed in the working assembly; re-copying the archive is not required. Backup copies of the changed files are located in `D:\CCZMP PROJECT\_backups\flight_mi2_20261011`. Manifest of changes - `tools\flight_work_20261011\manifest.json`. New files are deleted during a rollback, the old ones `configs/cczmp/transport.ltx` and `scripts/cczmp_trunk.script` are restored from a backup copy. You cannot remove a module from a save containing this helicopter without first deleting its instance or returning to the save before it was created.

The model and sound are based on standard game resources. Controller and skeleton adaptation - work for CCZMP. This prototype is not an R1 Mi-2 rig or port.

## Landing fix v0.2

Forced `attach_vehicle(..., true)` in engine 1.5.1 skips `CCar::attach_Actor`. Checking one link `get_current_holder()` gave false success. The standard non-forced landing and two invisible entry points near the cockpit are now used. Processing F is delayed until the button is released; The standard usage handler is disabled only for the Mi-2. Success is verified by the presence of the owner of the vehicle (`engaged`), and not just by the player's link. With loading, the pilot is re-attached in the normal way, since the engine loader also uses a forced landing. If the loader left the player without a physical body, a temporary transport link and a regular exit restore the body, after which the real landing is performed. A temporary link is not considered a successful landing. Further movement of the player is performed by the standard transport holder; There is no permanent teleport following the helicopter. Attitude stabilization remains active when the propeller is stopped; lifting force and translational thrust are equal to zero. The old Mi-2 format with zero entry points adds two door entries before creating the physical body; physical data content, ID, name, position and strength are preserved. The new entry points do not add physical mass or change the geometry/UV of the body.
