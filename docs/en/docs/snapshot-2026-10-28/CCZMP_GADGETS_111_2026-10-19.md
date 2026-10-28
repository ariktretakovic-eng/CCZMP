[Русский](../../../snapshot-2026-10-28/CCZMP_GADGETS_111_2026-10-19.md) · **English** · [Documentation index](../INDEX.md) · [Translation notes](../../TRANSLATION.md)

# Electronics, ZonaTaxi and 111 service - 10/19/2026

Status: implemented in working files, testing of game scripts continues. This document is not a statement that all scripts have already been tested.

## How to use

1. Use a phone, PDA, PDA, tablet or laptop from inventory. The home screen shows installed and allowed applications. Bottom buttons: Back, Home, 111. X and Esc close the screen.
2. Store: tabs “For you”, “Categories”, “Installed”, search in the field below. Compatibility, size, availability of money and free memory are checked by the existing electronics system. Clicking “Install” installs the actual device program.
3. F-zondroid uses a separate repository interface. Installation of the store itself via freedom-zonedroid.nchg and device restrictions are preserved. This is an in-game network; programs do not access real servers.
4. Settings → Appearance: font, scale, wallpaper and accent color. The condition is stored separately for each item. Regular, utility, Linux and Ghost environments have different palettes.
5. Public services → login to your own account: full name, organization, position, affairs, debts, search, detention, registered personal transport. If the character does not have a separate tax account, the interface reports the absence of data, rather than inventing a status.
6. Taxi Zone: select the final stop, wait for the car by the road, go to the passenger door and press “Get in”. The application reserves the nearest available existing W140. Cancellation is free before the start of the trip. Payment uses the existing taxi cash system; bank payment not added.
7. Emergency service: dial 111 or press 111 on the screen; choose ambulance, police or OMON. The call is free and available without a SIM when the charged device is on; Radio interference is interfering with the call. The call history contains the selected service and request.

## Interfaces

The new interface uses the native CUI of the engine window and DDS textures. Existing game operations are preserved. Separate views are made for stores, State services, NBZ, ZonaTaxi, calls, messages, contacts, files, notes, settings, browsers, terminal, Zenmap, network capture, calculator, maps and news. Professional programs use a common working layout with their own data and actions.

This is an adaptation of familiar interface schemes to the game. It is not an exact copy of all real application screens. Scan results, banking actions and other transactions refer only to game data NChG.

## Field services

The first stage of field trips and patrols is limited to the Dead City. At other locations, the call reports an unavailable route. Existing taxi routes in other locations have not been deleted.

| Service | Transport | Crew and mission |
|---|---|---|
| Ambulance | GAZelle NEXT, donor 206 | Driver and 3 doctors; exit on the right, first aid to the living wounded, examination of the dead |
| Police | Regular patrol car, donor 023 | Driver and 2 employees; stop shooting and arrest |
| OMON | GAZ Tiger, donor 209 | Driver and 3 fighters; reaction to the shootout participants |
| Paddy wagon | Donor 210 | Driver, guard, up to 8 places of detention; delivery to base IC |

Service vehicles are created by separate sections cczmp_service_ambulance, cczmp_service_police, cczmp_service_omon and cczmp_service_van. The original gaming machines and W140_SK have not been replaced.

The call is queued for 30–60 seconds of active game time. Then the vehicle appears on the surveyed road in a place hidden from the player and physically travels along the route. This is a delay before departure, the time of the trip itself is added. Sirens MVD, IC, ambulance and OMON are different; The siren of the away vehicle is turned off after arrival. Headlights are on.

First aid takes 20–30 seconds next to a living wounded person, after which health rises to at least 70%. Service does not revive the dead. An inaccessible target after 45 seconds without advancing is skipped without dummy healing. The ambulance also receives a request for an ongoing investigation IC.

Two patrols check documents in different parts of the city. The player is shown a verification window and an employee ID is available. Refusal, lack of your own document or a valid arrest warrant will lead to detention. There is a release of control when transportation is interrupted, a location is moved, and the maximum expectation is exceeded.

The police must detain the shooters and do not open fire. OMON uses standard combat AI against marked participants in the firefight. The loss of the entire police crew creates an urgent request OMON. The guarantee of arrival in exactly 30 seconds has not yet been confirmed: it depends on the available hidden space and travel.

## Saving engine state and restrictions

The state of devices, messages and calls, orders, requests, crews and transportation is stored in the existing serializable world cczmp_items. CUI windows, userdata and handlers are not written there. During a pause, service timers are not advanced.

The engine does not have a standard placement of a group of controlled NPCs as CCar passengers. Therefore, during the ride, built-in seated models associated with the actual ALife saveable crew characters are visible. When exiting, these characters are activated; the driver remains in the car. This is an implementation limitation, not a full native passenger system. Transporting the player uses a real car holder.

## Checks

Confirmed before the current pass:

- Lua 5.1 compilation of new and changed scripts; XML parsing; uniqueness of LTX sections.
- Four sections of official transport are registered; The four siren sound files differ in their hashes.
- Native rendering pass for 50 catalog programs; separate screens for phone, public services and network tools; the application button responds to a physical click; the window closes.
- Walking test: the doctor reached the goal, the employee MVD walked about 40 m.
- Controlled medical test 10/19 at 07:27:13: first_aid entry, application 67, target health from 0.18 to 0.70 in 20 seconds. This test confirms treatment near a doctor; The doctor’s approach to a stationary wounded person is still being tested separately.
- 47 main save and settings files have been hash checked and not changed.

Open checks: completion of detention/transportation, restoration of transportation after loading, full ordering of a taxi through the application, combat scenario OMON, absence of repeated native crash clsid after long work. Earlier, during the exit test, an access violation was received in clsid; The reason is being investigated using the dump. For now, this remains a known review issue rather than being announced as fixed.

## Files and recovery

Working materials and journals: tools/gadget_dispatch_20261019. List of installed files and checksums: installed.json. Source versions: _backups/gadget_dispatch_20261019_023257.

rollback.py by default only checks for rollback capabilities. It refuses to work when Anomaly is running or if the installed files have been modified by someone after this change. Explicit launch with --apply restores exactly this set of files and first saves their current copy. Basic saves and settings are not included in the rollback. Do not load a save with new items/crews after deleting their configurations; use save before this update.
