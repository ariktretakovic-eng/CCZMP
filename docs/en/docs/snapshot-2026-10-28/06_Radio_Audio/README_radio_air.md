[Русский](../../../../snapshot-2026-10-28/06_%D0%A0%D0%B0%D0%B4%D0%B8%D0%BE_%D0%B7%D0%B2%D1%83%D0%BA/README_radio_air.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# CCZMP: “Voice of Pripyat”, trunk and car IC

Changes for the current build of Anomaly 1.5.1. The pack of third-party machines was not connected as specified by the customer. The location of the IC base in Pripyat is awaiting coordinates.

## Use

| Action | Management |
|---|---|
| Open trunk | Approach behind the car, look at it, press F. On the left is the trunk, on the right is the player’s inventory. |
| Move item | Double click or drag between two inventories. Closing - ESC or button. |
| Car radio | The window appears after landing; again - ESC → “Car radio”. |
| Turn off car music | "On/Off" in his window. Leaving the car does not turn off the receiver. |
| World Radio | Go to the radio receiver and press F. New and previous receivers automatically connect to the air the first time they are detected by the new system. Manual shutdown is retained. |
| Radio PDA | Radio tab → CCZMP button. |
| Select song | Switch "Radio/Player" to "Player". There are no song selection buttons on the air. |
| Klaxon | Klaxon button in the car radio window; H with LuaJIT FFI support in the engine. |
| Mercedes IC | F7 → CCZMP transport → Mercedes-Benz W140 — IC. Regular debug spawner section: `cczmp_veh_w140_sk`. |

The trunk of a locked car is inaccessible until the car is unlocked. Items in slots and quest items cannot be transferred. The content remains in the save made after the transfer; An earlier save returns the previous composition. The original items, their condition and individual details are preserved.

## Ether

“Voice of Pripyat” is a cyclic program: call signs, music blocks, news, advertising. The overall position belongs to the saver, not the receiver. All receivers of one station use one position. Other locations are connected to this position when objects appear online; their broadcast does not start anew.

The timer moves while the world is running and is saved along with the game. After the game is closed, it does not continue to count real calendar time. loading of an earlier save returns the ether to its previous position. The snapshot also contains a record of the current fragment and milliseconds within the record for each station.

There is no audio rewinding in the installed Lua API. Therefore, records are pre-split into precise second-long OGG buffers; the next buffer is assigned to the common boundary with an engine delay. Joining in the middle of a second can result in a wait of up to one second. This is synchronization by program seconds; network synchronization between different instances of the game is not implemented.

Car sound is located near the car, follows it, becomes quieter after exiting and fades with distance. Far from the machine, the sound stream is released, but its “on” state and position continue. When you return, the radio plays the current part of the program. Removing the machine stops its sound.

`full` is available everywhere, `goska`/`gos` - in government areas, `crim` - in criminal areas. All channels and the general channel `all` are available in the car. The limit is determined by the base, not the player's organization. Currently, music sources are only available in `full`; special channels use common voice inserts before adding their own songs.

The first four voice inserts are recorded with temporary synthetic Russian voice acting. These are not actors' lines. You can replace them with your voice without changing the code. Before publishing a work, it is recommended to listen to and edit the content and voiceover.

## Adding entries

In the existing folder `_index/музыка для радио`:

- `full`, `goska` (`gos` is also supported), `crim` - MP3/OGG/WAV/FLAC/M4A music files.
- `voice_pripyat/jingles` - call signs.
- `voice_pripyat/news` - news.
- `voice_pripyat/ads` - advertising.

Replace or add files, then from the project root run:

```text
C:\Python314\python.exe tools/import_radio.py
```

The team updates the player and collects the broadcast. To change only inserts:

```text
C:\Python314\python.exe tools/build_radio_broadcast.py
```

To build you need FFmpeg: use an existing project tool, or pass `--ffmpeg ПУТЬ`. Do not run the import at the same time as the game. After importing, restart the game. The duration of the recording is rounded up to the nearest whole second, and the end is completed with silence.

The program order is stored in `gamedata/configs/cczmp/broadcast.ltx`; list of music sources - in `radio_tracks.json`. First come the call signs, after every two songs there are news and advertising; the last incomplete block also ends with inserts. Special channels without their own songs have a cycle of inserts.

## Mercedes IC and horns

Section `cczmp_veh_w140_sk`, catalog `w140_sk`, name "Mercedes-Benz W140 - IC". Geometry of the current W140; selected resources:

```text
gamedata/meshes/cczmp/vehicles/sk/mercedes_sk.ogf
gamedata/textures/cczmp/vehicles/sk/
gamedata/configs/cczmp/vehicle_physics/w140_sk.ltx
```

GPS, alarm and improved suspension are installed right away, including the usual ALife/debug spawn. The current CCZMP fuel system is retained: tank 100, consumption parameter in configuration 6.5, power in settings 408. These are game parameters, not certified real performance characteristics. The native GetfFuelConsumption() returns a normalized value of about 0.000065. The model uses the physics of the already improved W140. GPS is displayed by means of the existing transport system; Having an alarm installed does not mean that the car is always locked.

Place the source code for the horn IC here:

```text
_index/vehicle_horns/sk/horn.wav
```

`horn.ogg`, `horn.mp3`, `horn.flac` are also acceptable. One folder for each of the 41 organizations; identifiers match the registry of groups (for example `mvd`, `mchs`, `alfa`, `vympel`, `sk`). Import:

```text
C:\Python314\python.exe tools/import_vehicle_horns.py
```

The result is `gamedata/sounds/cczmp/vehicles/horns/sk/horn.ogg`. While there is no sound of its own, IC uses the common two-tone horn from `default/horn.ogg`. Regular cars use a common horn, or an organization directory if its identifier is assigned to a vehicle record. The unique signal IC is not invented instead of the customer's future file.

For future database scripts, an explicit spawn with specified coordinates and navigation vertices is provided:

```lua
local ok, message, id = cczmp_transport.spawn_organization("w140_sk", position, level_vertex, game_vertex)
```

Without building coordinates and checking room availability, interior design, staff and parking were not accommodated.

## Air transport

Theoretically, it is possible to create the basis for free flight, but the existing scripted helicopter itself does not provide a full-fledged controllable machine. The installed API includes setting the target, speed and altitude of the helicopter. For full-fledged free flight, you need separate controls, camera/pilot seat, takeoff and landing, collisions, damage, fuel and maintaining position. Depending on the required physics, engine changes will be required. Experimental flying vehicles are not added with this update.

## Installation and rollback

On the work computer, the update is already installed in `D:\CCZMP PROJECT`. Archive - a copy of the changed files for transfer/control. Unpack only into the same version of the assembly with previous CCZMP systems already installed. Backup copy of replaced files: `_backups/radio_air_20261010_195918`; its `manifest.json` distinguishes replaced files from new ones. Do not copy test saves into your game.

Checks and limitations are given in `verification/results.md`. Test launch scripts are not installed in `gamedata` from the archive.

## Confirmation after full restart

All 205 tests pass; 1075 installed files are verified using SHA-256. In the new game process, the saved broadcast position, radio on states, 17 units of fuel in Mercedes IC and the original trunk item with a state of 0.63 and an individual charge of 37 are confirmed. User settings are restored, user autosaves are not changed, temporary test scripts are deleted.

Complete new native boarding/exiting loop test harness did not confirm: direct attach_vehicle() did not board the player. Changing the volume and keeping it on are covered by automatic tests; the sound from outside the car is confirmed in the game. A separate native H press from the driver's seat has not been tested; The horn button works, reading H via LuaJIT FFI is available.
