[Русский](../../../snapshot-2026-10-28/CCZMP_VEHICLE_FIX_2026-10-18.md) · **English** · [Documentation index](../INDEX.md) · [Translation notes](../../TRANSLATION.md)

# CCZMP - tank and vehicle fixes

Date: 2026-10-18T01:27.
Model register: CCZMP_TRANSPORT_STATUS_2026-10-17.md.
Re-verification: all 46 sections, 53 OGFs and 43 donor ZIPs listed in the registry technical confirmations were found. Result: tools/vehicle_fix_20261017/status_recheck.json.
Backup: D:\CCZMP PROJECT\_backups\vehicle_fix_20261017_122708.

## Changes

- General physics of contact of wheels/rollers with a low obstacle: checking support, height, free space and speed; limited suspension forces without teleportation. The different axles of the imported skeletons and rear axles are taken into account.
- Permissible vertical step: up to 0.32 m for a car base, up to 0.65 m for a tank; actual passage depends on the geometry of the obstacle, overhang and available space. Full ground deformation and destructible walls were not added.
- Searching for a spawn location checks the entire size, ground difference, ceiling, cars and people; the initial roll/pitch is reset to zero. Connected to merchant/debugger, taxi, IC and garage cars.
- Healthy car: the first direct HE hit leaves 45% strength and turns on smoke; the second causes a regular explosion. A previously damaged vehicle may explode earlier.
- HE: radius 18 m, close lethal zone 6 m; walls shield, low shelter weakens. The surviving NPCs turn on the standard scheme of the wounded person asking for help.
- BB: holding fire gives automatic shooting with an interval of 200 ms, a visible flight trail and a hit effect. The HE remains single with a cooldown of 6.5 s.
- A character is hidden in the tank, active armor blocks bullet, explosive and impact damage to the main character. Penetrating the AP can damage the crew; destroying the vehicle kills those inside.
- Real NPC taxi crews/IC are taken into account, including temporarily offline; death is preserved by identity and is not replaced by a living driver after loading.
- Car explosion: death inside, lethal close range of 3.5 m and injury/concussion up to 12 m, taking into account shelters.
- Rear light sources are directed backwards, red and with shadows; The glow of the lenses is limited by the direction of observation. The lens material has been corrected from forced white selflight to a separate textured emissive material cczmp_vehicle_lens.
- The position of the luminous lenses has been specified based on the surface of the original body; changed glowing children of 47 OGF; original body parts, UVs and physical elements are preserved.

## Tank control

F - landing; X/F - output when stopped; J - engine; W/S/A/D - movement; space - brake; B - OF/BB; LMB - fire (holding works for BB); U - loading ammunition.

## Checks

| Script | Result |
|---|---|
| Lua 5.1, ballistics, cover, armor, safe spawn, directional light | Code checks passed |
| Tank, real curb 0.17 m | PASSED |
| W140, 0.17 m curb with 0.276 m local step | PASSED |
| Two HE, smoke/explosion, three real employees IC | PASSED |
| Red glow of W140 lenses, selection of binding based on two game frames | PASSED |
| Bullet hit on the main tank inside the tank | PASSED |
| BB burst, ammunition consumption | PASSED |
| loading of an occupied tank: armor, ammunition, engine, fuel | PASSED |
| Death of GG in the explosion of an occupied car | PASSED |
| Protected original save/settings files | 47 hashes match |

Individual profile tests: tools/vehicle_fix_20261017/native_appdata.
Detailed results: tools/vehicle_fix_20261017/final_verification.json.
The color and spacing of the lenses are verified from game frames; the subsequent fit to the body is checked geometrically for 46 adapted OGFs.

Actual render tests conducted in DX9; For the remaining renders, separate versions of the material have been prepared, but their launch requires separate verification.

Individual driving tests of all 46 transport sections were not carried out; general modification does not replace the customization of each donor body.

## Rollback

Close Anomaly and run python tools/vehicle_fix_20261017/rollback.py.
The script will check the hashes of installed files and backups before restoring them.
