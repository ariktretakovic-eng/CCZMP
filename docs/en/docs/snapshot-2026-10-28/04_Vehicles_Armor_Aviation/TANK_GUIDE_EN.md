[Русский](../../../../snapshot-2026-10-28/04_%D0%A2%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82_%D0%B1%D1%80%D0%BE%D0%BD%D0%B5%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0_%D0%B0%D0%B2%D0%B8%D0%B0%D1%86%D0%B8%D1%8F/TANK_GUIDE_RU.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Tank NChG – STALKER X CCZMP
## Receiving
F7 → “CCZMP: create tank NChG.” The car appears on a free area in front of the player. Available to the military department in the general transport catalogue. Section: cczmp_veh_tank. The base model is extracted from the game's static tank; the original map objects have not been replaced.
## Management
Approach the hatch from the side, look at the hull and press F. One player position: the driver simultaneously controls the gun.
W/S - forward/backward; A/D - separate control of the sides, including turning on the spot; space - brake.
J - engine; mouse - turret guidance; LMB - shot; B — selection of OF/BB; U - load shells from inventory.
F/X - leave a stopped tank if there is a free exit point nearby. Standard 1/2/3 — cameras; L - light; G - horn; R - radio.
## Game parameters
Weight 40,001 kg, 16 physical rollers, separate left and right side drive. Setting speed: up to 12 m/s forward and 4 m/s backward. Actual speed depends on contacts, slope and damage.
Tank 650 l; The existing fuel and vehicle repair system is used. The engine rating in configuration is 750 hp.
Ammunition capacity: 36 rounds, when creating 12 HE and 12 AP. Reload time 6.5 s. Changing the type does not reset the cooldown.
Separate items cczmp_ammo_tank_he and cczmp_ammo_tank_ap, one shell per package, weight 20 kg. F7 produces six of each. For loading, press U in the tank: items are consumed, the ammo counter increases to the total capacity.
Initial speed: HE 850 m/s, BB 1200 m/s. HE radius is 12 m, damage decreases with distance, walls and equipment block the explosion. BB takes into account the side of the armor, angle and speed; a single ricochet is possible with a glancing hit. The durability of the armor is determined by game coefficients, not by millimeters of real armor.
The engine, left/right drive and turret are in separate condition. Damage limits movement and shooting. Overall strength remains the vehicle's standard strength. Regular repairs also restore damaged components; A complete body restoration completely restores the components.
## Device
cczmp_tank.script - object binding, landing/exiting, roller drive, control, status, HUD.
cczmp_tank_ballistics.script - flight of projectiles, continuous checking of intersections, explosions, armor, effects.
cczmp_armor_math.script - integration of trajectory with gravity and resistance.
cczmp_tank_debug.script - F7 commands.
configs/cczmp/tank.ltx - parameters for movement, ammunition and armor.
configs/models/vehicles/cczmp_tank.ltx - car physics, engine, suspension, light, turret, sound.
meshes/cczmp/vehicles/armor/tank_nchg.ogf - a new skeletal model with physical rollers and a rotating turret/barrel.
## Saving
Ammunition, selected projectile, reload time, modules and sight are tied to the server object of the vehicle. Fuel is preserved by the existing transport system. The flight of fired projectiles is stored in the world data and restored within its location. Content from a later save does not carry over to an earlier save.
## Implementation boundaries
This is a basic game tank, not a certified model of a specific model. The texture and shape are taken from the game. The track surface is still visually solid, the rollers are physically moving; There is no separate simulation of each track. The general physics of the world has not been replaced. This is not a package of self-propelled guns and radars.
