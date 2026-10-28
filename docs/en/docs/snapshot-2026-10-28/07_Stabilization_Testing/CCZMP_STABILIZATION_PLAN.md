[Русский](../../../../snapshot-2026-10-28/07_%D0%A1%D1%82%D0%B0%D0%B1%D0%B8%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B8/CCZMP_STABILIZATION_PLAN.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# STALKER X CCZMP - stabilization and the first working city

Date: October 12, 2026, user time. Version 0.1.

Basis: attached master concept version 0.1. This is a proposal for the sequence of work and readiness criteria. Long-term ideas, details and proposals from the concept retain their original statuses; the document does not declare them to be implemented or automatically approved requirements.

## 1. What can be done

A significant part of the offline systems can be developed on the existing assembly: NPC personality and memory, schedules, events, property, rent, professions, local economy, documents, game investigations, services and interactions with transport. Each block should end with a running game script and a check of saves.

| Direction concept | Nearest useful result | Condition for further development |
|---|---|---|
| Stable offline | Reliable interfaces, saving, operations with items and money | acceptance testing current mechanics in the game |
| NPC Life | Multiple characters with memories, needs and schedules | Limited scheduler and compatibility with existing AI schemes |
| Real estate | One property with owner, rental, access and storage | Marking of specific existing premises |
| Professions and economics | Courier, mechanic and investigator with different work actions | Unified rules of payment, items and rights |
| State and crime | The case connects the event, evidence, document and employee decision | Formalized powers and game rules of evidence |
| Land and air transport | Bringing existing vehicles and Mi-2 to reliable user scenarios | Separate check of each model, transitions and saves |
| New areas and transport networks | One prepared area or short route | Working with resources, SDK and navigation based on research results |
| Trains and free walking inside | Separate experience with one moving platform and passenger | Check for relative motion, collisions, jumps and loading; then decide on engine changes |
| Online | Small Authority Server Prototype | Proprietary architecture, synchronization and load sensing |

1000–2000 concurrent players is a research and scaling goal. Now it is impossible to promise such capacity or the transfer of offline systems to online without reworking.

## 2. What you can already rely on

The following reasons are read in the current working assembly files on KOMPUTER:

| Module | Found base | What this doesn't confirm |
|---|---|---|
| `cczmp_items.script` | ALife storage, serial numbers, item verification by ID/name/owner, protection of consumables from reuse, log of the last 100 entries | A single long-term journal of the entire economy and history of the world |
| `cczmp_ops.script` | Persistent person keys, link re-resolution, authority checks | Full biographical memory and independent life of NPCs |
| `cczmp_professions.script` | NPC Service Roles, Organizations, Ranks and Service Scheme | Complete work schedule, career and salary for each NPC |
| `cczmp_bank.script` | Banking module and saved record numbers | General economy of all NPCs and enterprises |
| `cczmp_transport.script` | Catalog, acquisition, rental, owner and departmental transport records | Urban traffic and universal passenger transportation |
| `cczmp_vehicles.script` | Recovering and storing fuel at a server facility | Reliability of all future transport models |
| `cczmp_trunk.script` | Transfer of real items, access check, incomplete operation status | Complete acceptance testing of all transfer boundary cases |
| `cczmp_ui.script` | Terminal and close, navigation and confirmation handlers | General input ownership policy for all windows |

This is a source cut, not a new complete acceptance testing assembly. In the previous stage, the Mi-2 was tested separately: actually pressing F, flight, loading, exit and restoration of the old physical state format. Such checks should be saved as regression scripts.

## 3. Stage S0 - stabilization of existing systems

### S0.1. Record the initial state

- Module registry: purpose, dependencies, game triggers, data format, versions and passed checks.
- Backup of modified files and checksums; separate copies of saves for testing.
- Separate the statuses “described”, “in the code”, “works in the prototype”, “tested in the game”.
- Check Russian localization files taking into account the required Windows-1251 build and XML declaration.

### S0.2. Interfaces and input proficiency

Coordinate the opening and completion of documents, gadgets, trunk, radio, terminal and debug. A window should release only the input capture it owns. Losing an object, loading, character death, and normal closure should lead to a certain state.

acceptance testing: open a document → close with the button or Esc → use the item and its properties → open F6 and F7 → open the gadget → close it → interact with the machine. Repeat the sequence several times. Check the provided transitions between windows and the absence of repeated action from one press of F.

### S0.3. Conservation and identity

Use a permanent logical key of a person or thing where a long-term history is required. Check the link to the engine object using a set of identifying fields; a numeric ID by itself is not sufficient. Save data, not live Lua/engine objects.

Add format versions and explicit migrations. Removing an NPC or vehicle must clear or archive associated records according to system rules.

acceptance testing: save after changing → close the game → load → compare state. Then load an earlier save: changes made after it should not be present. Check for an object leaving the active simulation and returning, as well as removing and reusing IDs.

### S0.4. Operations with objects and money

To transfer, pay and issue the result, a single order is needed: check → reservation or wait record → execution → confirmation. When interrupted, the operation must complete once or be restored to its original state. Use the existing checks and status `pending` as a basis.

acceptance testing: double confirmation, disappearance of the seller, removal of the required tool, item has already been transferred, loading while waiting, lack of money, lack of space to create the result. The balance and number of copies must correspond to the actual completed actions.

### S0.5. Events, timing and diagnostics

- Describe the events: source, participants, location, playing time, result and operation ID.
- Coordinate hours for rentals, fines, credits, charging and future schedules.
- Set event reprocessing rules and history restrictions.
- Separate the diagnostic error log from long-term game memory.
- Native errors cannot be declared fixed only based on the result of a test with substituted APIs.

acceptance testing S0: control game scenarios pass, changes are saved and rolled back along with the save, known errors are reproduced or have a confirmed fix, control is available after closing the interfaces.

## 4. Stage S1 - NPC with memory and schedule

First experience: 3-5 specific NPCs in Dead City, next to the already selected base IC. Do not enable the new simulation for all Anomaly characters at once.

Each character has:

- Permanent identity and current role; name, organization and place of work.
- Several traits: gullibility, caution, sociability. Separately - fatigue, stress and current need.
- Home or place to sleep, work point, time of work and rest.
- Short meaningful memory: help, threat, work done, duty, evidence of an event.
- Attitude towards the player and one or two other characters.
- Limited set of actions and transitions compatible with existing AI schemes.

Example: a mechanic goes to work in the morning, accepts repairs, receives payment, remembers the completed order, and leaves to rest in the evening. If the player previously helped him, the response or available service changes. The same episode with loading should not re-charge payment or memory.

Near the player, actions are performed in the game world; A limited set of data is updated for a missing character. A distant NPC should not require constant physical simulation. The frequency and budget of updates should be selected based on measurements on the user’s computer.

acceptance testing: NPC executes schedule, reacts to event, retains memory after restart; leaving a location and returning does not create duplicates of the character, money or events. Without the player's order, the NPC is able to perform at least one useful action.

## 5. Stage S2 - one city with related mechanics

Suggested first set: Dead City; existing database IC; one workshop; one delivery point; one accessible room with storage.

| Script | Player Actions | Communication with other systems |
|---|---|---|
| Courier | Accept an order, receive a cargo, deliver to a specific addressee | Real Item, Trunk, Recipient, One Time Payment |
| Mechanic | Diagnose the malfunction and perform repairs | Tools, materials, skill, transport, payment |
| Investigator IC | Receive a message, collect information, file a case | NPC Identities, Documents, Authorities, Evidence and Decisions |
| Tenant | Get a room for a period of time, open access, store things | Owner, contract, money, access rights, conservation |

First, agree on the game rules of evidence: source, time, related episode, authenticity, official access, verifiability. Changing an NPC's attitude in itself should not automatically be considered a proven crime.

acceptance testing: the player receives an order → uses transport and trunk → delivers the item → receives payment → pays rent → saves → restarts the game. All connected systems reflect the same complete story.

## 6. Selected technical prototypes

### Moving platforms and trains

Start with one platform, one character and a short path. Check standing, walking, crouching, jumping, collisions, braking, leaving the platform and maintaining while moving. Based on the results, determine the necessary engine changes. New paths, stations and navigation require independent preparation of resources.

Before these checks, a full-fledged free-running train cannot be declared ready.

### Air and water transport

Use the Mi-2 as an existing piloting prototype. Passengers, NPC pilots, flights between levels and new air models are independent expansions. Water transport starts with one hull and a tested buoyancy model on a specific body of water.

### Online

First, remove the rules of operations from the interfaces and separate the data from the engine objects. Then create a small network experience: two clients, authoritative transaction verification, one item, one transfer, one transport object. After that - load, recovery from failures and scaling up. The number of supported players can be determined by measurements.

## 7. Operating assumptions for the first stage

- Offline first; maintain the existing division into levels.
- The first populated area is Dead City.
- Existing banking system, fuel, documents and items to be expanded through adapters and agreed upon rules.
- Mass population, new megacities, hundreds of professions and permanent death will be introduced after checking the basic scenarios.
- Relationships, characters, memories and properties should be data that can be saved and later checked on the server.

These assumptions allow stabilization to begin. Open concept questions about online, inheritance, time scale and seamlessness remain separate solutions.

## 8. What to do first

Start with S0: register of existing mechanics and regression acceptance testing of interfaces, inventory, money and saves. Then implement S1 on several NPCs. The first outcome criterion is a working city from S2, where already existing objects, transport, organizations and documents participate in a common story.

No game files were edited in preparation for this plan.
