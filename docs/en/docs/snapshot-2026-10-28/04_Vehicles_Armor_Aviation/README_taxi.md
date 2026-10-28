[Русский](../../../../snapshot-2026-10-28/04_%D0%A2%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82_%D0%B1%D1%80%D0%BE%D0%BD%D0%B5%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0_%D0%B0%D0%B2%D0%B8%D0%B0%D1%86%D0%B8%D1%8F/README_taxi.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Taxi - STALKER x CCZMP / Anomaly 1.5.1

Development 10/12/2026. Checks are still being carried out; service readiness has not been confirmed.

## Usage

Two taxis are created when visiting Dead City. The cars use the body of a regular W140. W140_SK and personal W140 are not replaced.

Go to the right door of a stopped taxi and press F. In the menu, select a stop and press “Let's go.” On the way, X requests to stop and exit. ESC opens a normal pause, and in the order menu cancels the landing. There are car marks on the map; A separate taxi search item has been added to F7.

Stops: street near the base IC, eastern quarter, central square, northern quarter, western quarter, southern quarter. The route is fixed; The menu displays the actual path length and price.

Payment: 100 rubles per submission + 0.75 rubles per meter of route, rounded up to 10 rubles. Payment is debited upon departure. If you leave early, the remaining amount is returned; if the trip is unsuccessful, the full cost is returned. Repeated calculation of the refund is blocked by the calculation record.

## Implementation

Sections: cczmp_veh_w140_taxi and cczmp_taxi_driver. Permanent records of cars, drivers, orders and payments are located in cczmp_items.world().taxis. The movement is carried out by the forces of the physical shell and the motors of the steering joints. Landing uses a standard CCar, the player's seat is on the right. Sections of the path follow level collision data; it is a vehicle route, not a pedestrian route.

The driver is a saveable NPC. When in motion, it is switched offline and displayed as a seated representative of its model in the back; At the bus stop he appears next to the car. This is a bypass for the restriction of the regular CCar slot intended for the actor.

The trunk contents, fuel and radio use existing assembly systems. After boarding a taxi, the destination menu first opens; The radio can be opened separately in the standard way.

The sources of W140 and W140_SK have not been changed. Backup of replaced scripts and configuration: D:\CCZMP PROJECT\_backups\taxi_deadcity_20261012. The old experimental zz_cczmp_taxi_test.script is disabled; its source is saved in a backup copy.

## Checks

Lua 5.1: module syntax and five checks for route calculation, price and physical limitations passed. The appearance of cars and NPCs, boarding, a menu of six stops, failure due to lack of money, one-time write-off and a trip with a passenger about 80 meters through turns are natively confirmed. loading is in the middle of the trip and the full cycle of both cars is still being checked. The player's original saves and settings are retained; game checks are performed in a separate profile.
