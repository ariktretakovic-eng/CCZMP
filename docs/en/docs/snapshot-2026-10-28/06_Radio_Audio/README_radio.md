[Русский](../../../../snapshot-2026-10-28/06_%D0%A0%D0%B0%D0%B4%D0%B8%D0%BE_%D0%B7%D0%B2%D1%83%D0%BA/README_radio.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# CCZMP - radio and directory PDA

Installed in `D:\CCZMP PROJECT`. The archive contains files for overlaying the current build and five ready-made OGG tracks. Close the game before manually copying `gamedata` and `tools` to the project root.

## Management

| Where | How to open |
|---|---|
| PDA / PDA | Standard tab “Radio” → “CCZMP: stations NChG” |
| Radio in the world | Come within 2.5 m, look at the radio and press F |
| Car | While in the car, press R |
| Pocket Radio | CCZMP music radio action in inventory |
| Debugging | F7 → CCZMP items → “Create a radio in the world”; also section `cczmp_radio_world` in the regular spawn catalog |
| Directory | PDA → “Directory”: five new CCZMP categories |

Power, station, previous/next track and volume are available in the interface. Esc and the Close button close the window; The sound continues to play as long as the receiver is turned on. Exiting the car stops in-car playback. When re-landing, the switched on radio starts the selected track from the beginning.

## Stations and territory

- `full` - available everywhere.
- `goska` and its alias `gos` are state territories.
- `crim` - criminal territories.
- All stations are available in the car; by default, the general list “All stations” is selected.

The territory is determined by the nearest simulation base within 80 m and its owner. CCZMP state/criminal communities are identified by the registry of organizations. For regular communities, military, scientists and IIG are considered state, bandits and renegades are considered criminal. Outside the base, only `full` is available; the passing NPC and the player's organization do not change the owner of the territory.

If necessary, set the exact ownership of a specific database in `[territories]` of the file `gamedata\configs\cczmp\radio.ltx`: `имя_smart_terrain = f_mvd`. The remaining bases use the actual owner of the simulation. Importing music saves these settings.

Physical receivers automatically appear when approaching up to 150 m to simulation points with a base sign. The existing registered radio within 80m is being reused. The model of the new objects is the standard Anomaly radio; no separate models were created. The choice of station, power, track and volume belongs to the current save. loading of an earlier save returns the previous settings; The audio position by second is not saved.

## Adding music

The source files are located at `_index\музыка для радио\full`, `goska`/`gos` and `crim`. Currently provided **five tracks in full**; The state and criminal folders are still empty. The empty station displays a message and remains safely silent.

1. Add MP3, OGG, WAV, FLAC or M4A to the desired folder.
2. Close the game.
3. In the project root, execute `C:\Python314\python.exe tools\import_radio.py`.
4. Start the game again.

The project ffmpeg is installed on this PC via `imageio-ffmpeg`; the importer will find it automatically. On another PC you can transfer `--ffmpeg ПУТЬ_К_FFMPEG.EXE` or install `imageio-ffmpeg`. The importer converts the music to OGG Vorbis 44.1 kHz mono, adds X-Ray audio parameters and updates the catalog/track titles. The music is common to PDA, bases and vehicles, so separate copying for vehicles is not required.

## Reference and titles

Added **311 articles**: 9 articles of NChG/Constitution, 73 articles of laws, 41 organizations, 186 items and 2 instructions. Articles are available immediately, including existing saves. Description of the organization, ranks and equipment, texts of norms, punishments and characteristics of items are read from the current configs. Previous Anomaly articles have been preserved.

The display name of the "Dolg" faction has been changed to "PMC X-Soldiers" in Russian names, descriptions and lines. Internal ID `dolg`, relationships, jobs and saves retain the same structure. Monetary debt and bank symbols have not been renamed. The previously recorded original voice acting remains the same.

Backup before installation: `D:\CCZMP PROJECT\_backups\radio_reference_20261010_174045`. For renamed texts, the source code and a separate manifest are preserved.
