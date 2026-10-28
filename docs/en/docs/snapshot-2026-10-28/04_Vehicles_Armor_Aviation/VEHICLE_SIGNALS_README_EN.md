[Русский](../../../../snapshot-2026-10-28/04_%D0%A2%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82_%D0%B1%D1%80%D0%BE%D0%BD%D0%B5%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0_%D0%B0%D0%B2%D0%B8%D0%B0%D1%86%D0%B8%D1%8F/VEHICLE_SIGNALS_README_RU.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Light and transport signals - 10/16/2026

Management:
- Hold G in the car - horn/SGU. Release G—stop the hand signal.
- R in the car - open the radio. The automatic window after landing has been removed.
- Standard flashlight/headlight key (L by default) - simultaneously switch the beams and luminous surfaces of the flashlights. This control does not affect a player on foot.

NPC drivers receive mandatory low beams through a common controller. For the future controller: `cczmp_vehicle_lights.driver(car, true)` needs to be updated during control, including waiting and parking. Calls `cczmp_taxi.drive_external` already do this. The engine of a regular car also turns on the lights automatically unless the driver has manually selected the state. Manual state is stored in the server object data.

The headlights have a standard beam, their own luminous surfaces and halos for the renders that support them. The taillights have red luminous surfaces and red lighting near the vehicle. The placement settings are located in `gamedata/configs/cczmp/vehicle_lamps.ltx`. 46 model options included. Each option adds four small surfaces and one bone without collision or mass. The original meshes, UVs, bones, skins, crew and collision data are stored byte by byte.

IC: A separate 3D car quack works during the travel and parking phases. After the transition to inspection, it turns off. When you start leaving, another spatial sound is turned on once - distant city sirens. The event flag is saved with the case, so loading does not repeat the background fill that has already been heard. The onboard siren resumes if the loaded crew is still traveling.

Organization sounds: `gamedata/sounds/cczmp/vehicles/horns/<organization>/horn.ogg`. There are records IC, MVD, MChS and the Ministry of Health; other government organizations use the common entry `state/horn.ogg`. Civilian cars use a regular horn. Donors converted to OGG 44100Hz mono with X-Ray metadata; original MP3s are preserved. `audio_manifest.json` links all 27 prepared files with sources. Additional horn MVD and rail vehicle entries are prepared as resources; Independent new scenarios for their use are not included in this task.

Quiet urban background works in Dead City, Rostok and two city locations in Pripyat. The time of day determines the day/night set. Configuration: `gamedata/configs/cczmp/vehicle_audio.ltx`. A separate background exit siren is located in `cczmp/world_sounds/dispatch/sirens.ogg`.

Manual and service sirens are taken into account independently: releasing G does not interrupt the active exit IC. Sounds and light sources are not recorded as userdata in the save. The hand signal stops when you exit the machine, lose focus, and open the interface; loading clears temporary audio objects. Destroying and going offline a car removes its sound and light sources. There is an active time limit for manual signal and NPC request to prevent the sound from freezing.

After installation, you should restart the game; no new game required. The source files are in the backup specified in `baseline.json`. Checks and installation results - `test_report.json`, `asset_validation.json`, `model_validation.json`, `release_report.json`.
