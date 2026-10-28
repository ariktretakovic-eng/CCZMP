**Русский** · [English](../../en/docs/snapshot-2026-10-28/04_Vehicles_Armor_Aviation/vehicles_work__README.md)

# CCZMP W140 vehicle adaptation

Source: Mercedes-Benz 600 SEL (W140), saaake (@okbrobye), Sketchfab UID 86ae3dd6729441a09929566cababf77b. License CC-BY-4.0; see project CREDITS_VEHICLES.md and source/w140/license.txt.

Installed section: cczmp_veh_w140. The stock vehicles are preserved. F7 spawner categorizes SCRPTCAR sections as Vehicles. Debug mode must be enabled.

Pipeline:
- source/w140/scene.gltf and scene.bin: supplied original model.
- normalize_preview.py: bake glTF transforms and normalize length to 5.213 metres.
- convert_w140.py: restore missing three wheels using the original front-left tire and rim; mirror geometry and normals; retain body, cabin and UVs; adapt the native 16-bone car skeleton; assign rigid vertex weights; export OGF.
- w140_native.blend: editable model and native skeleton.
- w140_native.object: X-Ray editable object converted from the exported OGF.
- stage/gamedata: installable model, 24 DDS textures, configuration, localization and fuel persistence binder.
- last_backup.txt: exact backup folder. Its manifest records installed files, prior existence and SHA256; original resources, savedgames and logs are backed up.
- conversion.json and export_inspection/structure.json: geometry and bone reports.

Initial game tuning: rear-wheel drive, automatic four-speed gearbox, 2190 kg mass, 100-litre tank, separate engine and gear parameters. The engine's power/RPM/consumption units differ from a real vehicle simulation; numbers are initial game tuning.

Current limitations:
- 113933 triangles, 30 mesh batches; no LOD. Suitable for testing one vehicle; large fleets require optimization.
- Doors have no complete opening animation; two native entry-door bones are present, rear doors are fixed geometry.
- Stock engine sound is reused; this is not a recorded Mercedes V12.
- Static fallback replaces the source's runtime dashboard render target.
- The source mesh width including mirrors is 2.239 m. Original body proportions are retained.
- Car physics and colliders use the native X-Ray vehicle implementation with adapted geometry, mass and wheel positions. They passed single-vehicle runtime checks in Rostok; handling still needs broader tuning.

Installed files:
gamedata/meshes/cczmp/vehicles/w140/cczmp_w140.ogf
gamedata/textures/cczmp/vehicles/w140/*.dds
gamedata/configs/models/vehicles/cczmp_w140.ltx
gamedata/configs/items/items/items_cczmp_vehicles.ltx
gamedata/configs/text/{rus,eng}/st_cczmp_vehicles.xml
gamedata/scripts/cczmp_vehicles.script
CREDITS_VEHICLES.md

Runtime evidence: engine_checks.log, verified_engine.log and engine screenshots (when produced). CHECK_COMPLETE means the temporary probe completed; failures are logged explicitly. Regression results: regression_tests.log.

The separate cczmp_vehicles binder inherits the native car binder. Fuel uses versioned ALife server-entity storage, with snapshots before saving and going offline. Restore happens once the CCar exists. Older saves without this record retain native default fuel behavior. Stock vehicles use their original binder.

## Verified runtime
AnomalyDX9AVX: native CCar spawn, engine start, 6.75 m physics drive, warm/cold save reload with fuel 63.5 L and health 1. Player entered via F, started the engine via O, reversed about 12.9 m via S, drove forward with steering via W/A, braked via Space, stopped the engine and exited via F. Final session contained no fatal or Lua runtime errors. See runtime_verification.json and verified_engine.log. All 100 project regression tests passed. The temporary script was removed; vehicle test saves were moved to verification_saves. Original user saves match their pre-test hashes.

## Spawn and controls
Enable debug mode, open the F7 spawner and search W140 in Vehicles. Section: cczmp_veh_w140. Stand close to a front door and aim at the car; F enters/exits, O toggles the engine, W/S forward/reverse/brake, A/D steering, Space handbrake, L headlights. Do not spawn a car in an interior or against a wall.
