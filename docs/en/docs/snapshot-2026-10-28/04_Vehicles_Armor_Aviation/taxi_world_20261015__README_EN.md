[Русский](../../../../snapshot-2026-10-28/04_%D0%A2%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82_%D0%B1%D1%80%D0%BE%D0%BD%D0%B5%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0_%D0%B0%D0%B2%D0%B8%D0%B0%D1%86%D0%B8%D1%8F/taxi_world_20261015__README_RU.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# taxi world 20261015  README EN

Taxi in open locations - 10/15/2026

There are three W140 Taxi (69 cars) at 23 open locations.
Spawn is performed when visiting the location for the first time, numbers and NPC are saved
in existing cczmp_items.world().taxis. Revisiting does not create copies.
Two old taxis Dead City retain numbers, cars, drivers and payment;
a third car is added to this map.

F for a standing taxi - boarding and automatic menu for the final stop.
Select the line and press “Confirm Destination” or Enter.
The menu indicates the distance and cost. Money is written off once.
Esc—cancel boarding/exit. X while traveling - please stop.
Stops refer to the current location; interlocation transportation has not been added.
The position of the taxi can be seen from the markers on the map. F7 has a transition action
to the nearest taxi at the current location.

There are 6 stops saved in Dead City, 3-4 on other maps.
The routes are formed using level.ai and level.cform surfaces.
Outside the current location, taxi physics and drivers are disabled:
there is no simultaneous simulation of all 69 cars.

Laboratories, dungeons, fake_start and Hospital are excluded.
There is no connected passage of width W140 in the Hospital: after inspection they remain
only isolated small areas. There is no car parking there.

Files: gamedata/scripts/cczmp_taxi.script, cczmp_taxi_ui.script,
cczmp_taxi_routes.script, configs/text/rus/st_cczmp_taxi.xml.
The regular W140 and W140_SK are unchanged.
Syntax and logic modeling: verification.json.
Full native passage of all routes requires verification in the game.

Final verification: {"installed": true, "spawn_native": true, "boarding_native": true, "drive_native": true, "protected_files": 726, "cleanup": true, "locations": 23, "taxis": 69, "protected_unchanged": true, "installed_verified": true, "geometric_spawn_positions": 69, "native_fatal_errors": false}
