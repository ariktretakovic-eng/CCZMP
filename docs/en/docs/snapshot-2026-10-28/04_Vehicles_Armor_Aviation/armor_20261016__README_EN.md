[Русский](../../../../snapshot-2026-10-28/04_%D0%A2%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82_%D0%B1%D1%80%D0%BE%D0%BD%D0%B5%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0_%D0%B0%D0%B2%D0%B8%D0%B0%D1%86%D0%B8%D1%8F/armor_20261016__README_RU.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Heavy equipment: resource checking and calculation stand

Date: 10/16/2026. Project: STALKER X CCZMP, Anomaly 1.5.1.

## What has actually been done

Tested 4248 individual OGFs from gamedata/meshes and tools/_unpacked/meshes. There is no separate skeletal model of a standard tank with the veh/veh_tanchik texture among them. Found tank geometry in compiled maps: l07_military (visual 9092 and 9094), l10_radar (12907), l10_red_forest (17059). These are static MU objects of type TREE_ST, without skeleton, car physics and weapons.

From l07_military, visual 9094, 6373 vertices and 4945 triangles are extracted. UV, original geometry and texture are preserved. Files tank_extracted.blend, tank_extracted.obj, tank_extracted.mtl, tank_texture.png, tank_extracted.json. This is a source for conversion, not a ready-made driving tank. Export coordinates: Blender, Z up. No transformation is applied to the map instance: the local geometry of the model is used.

cczmp_armor_math.script - separate stand on Lua 5.1: integration of RK4 trajectory with gravity, quadratic resistance and wind; carrier speed inheritance; segmentation up to 2 ms for subsequent collision checking; analytical trajectory without resistance; calculation of springs and dampers; separate left/right track commands; in-game explosion damage decay; radar range and line of sight filter.

The stand is not installed in gamedata and does not trigger game events. It does not create projectiles, damage, or radar blips on its own. New heavy equipment has not yet been added to F7. The original game files were not changed at this stage.

## Checking calculations

Run: python tools/armor_20261016/test_math.py. Result: math_test_report.json. The analytical solution of motion is tested at different speeds, accelerations and variable frame times; continuity of segments; resistance braking; platform speed inheritance; static load and damper sign; turning the tracks on the spot; explosion and radar boundaries; incorrect arguments. These are numerical tests, not a test of the tank in the game.

Gravity acts immediately after crash. With a horizontal shaft and without air resistance: t = distance / speed, reduction = g * t² / 2. For example, for a conventional speed of 1000 m/s and g = 9.81: at 100 m the reduction is 0.04905 m, at 500 m 1.22625 m, at 1000 m 4.905 m. This is a sample calculation, not approved Performance characteristics of any ammunition. The sight zero and barrel angle change the position of the hit relative to the aiming line. In a working implementation, g must be taken from the current physical world and not changed globally.

blast_factor sets the game curve (1-d/r)^2 and the openness multiplier; This is not a calculation of the pressure of a real explosion. The radii and damage of different ammunition must be adjusted separately. Obstacles must be checked by the game adapter: one radius without taking into account walls is not enough.

## What is confirmed in the API and code

The supplied lua_help.script contains CCar, HasWeapon, Action, SetParam and control of physical joints via set_max_force_and_velocity. The reference CarWeapon.cpp has separate vertical and horizontal aiming bones and muzzle point, angle restrictions and aiming speed. Its stock OnShot uses FireBullet; This is not a ready-made heavy artillery shell. The CCar suspension requires physical wheel bones and wheel-joints; spring_factor, damping_factor and friction_factor parameters are provided.

Reference sources: https://github.com/themrdemonized/xray-monolith/blob/master/src/xrGame/CarWeapon.cpp and CarWheels.cpp; local copies are here. The current thread serves as a reference. The compatibility of each additional export with the installed binary must be checked in the game; The presence of a function in the new source does not in itself guarantee this.

## Next game prototype

1. Prepare the geometry: select the hull, turret, barrel, rollers and belts; check for completeness; make physical shapes, masses, low center of gravity, entry/exit points and camera. Determine the scale after visual inspection.
2. Test one steerable chassis on level ground, slope, curb and collision. We need separate drive of the sides and turning on the spot. The first version can be built on road wheels and a visual tape; the physical chain of individual tracks is a separate complex task.
3. Add a turret with limited aiming speed and a vertical barrel. Then ammunition, reloading, recoil and a separate type of heavy projectile with checking each segment of the trajectory. You can't just move a grenade to a selected point - that's how the old cczmp_emplacement prototype works now.
4. Implement game zones for damage to the hull, turret, chassis and engine; different hit and explosion effects; preservation of fuel, condition and ammunition; check output/loading and F7.
5. After one tested tank, transfer the base to a tank destroyer, limiting the guidance sector, and to other chassis. Radar is a separate module: power supply, viewing period, range, target class, visibility and contact lifespan. The presence of the Tor-M1 model in donors does not mean the readiness of the radar or air defense.

A global rework of gravity or physics of all cars is not required for the first prototype. The real simulation of a projectile only works in the active location; interlocation fire and equipment outside the online zone will require a separate abstract simulation. Native testing of the chassis, suspension, turret and hits is still ahead.

## Prepared corrected geometry

In the source code, one track is actually torn off: part of the tape lies on the ground. In a separate copy of tank_track_restored.blend / tank_track_restored.obj, the damaged tape is replaced with a mirror copy of the intact tape. The exact numbers of vertices and triangles are listed in tank_repair_report.json; the fingers of the damaged caterpillar remaining on the ground were separately removed. The source tank_extracted.blend is saved separately. Physics and skeleton are missing yet; This is the preparation of a resource, not a tank in the game F7. The images tank_extracted_preview.png and tank_track_restored_preview.png allow you to compare the result.

Ammunition should be divided by game role: armor-piercing - direct hit and a separate penetration/internal damage model; high-explosive fragmentation - explosion and fragments, taking into account shelters; smoke - own effect. There is no universal radius for all projectiles. A tank destroyer can use the same flight calculations with a different guidance sector and layout. The explosion radius, penetration, reloading and stock of shells have not yet been declared ready for performance characteristics.
