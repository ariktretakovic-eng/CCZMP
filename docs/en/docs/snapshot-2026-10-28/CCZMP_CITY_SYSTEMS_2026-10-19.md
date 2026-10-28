[Русский](../../../snapshot-2026-10-28/CCZMP_CITY_SYSTEMS_2026-10-19.md) · **English** · [Documentation index](../INDEX.md) · [Translation notes](../../TRANSLATION.md)

# CCZMP: city systems - 10/19/2026

## Contents of the update

Eight agreed areas have been implemented. Add-ons connect to existing CCZMP systems, inventories, economies, services and Anomaly 1.5.1 saves. The main user input is the “City NChG” application on gadgets. It automatically appears on previously created devices. Sections are available depending on the character's rights and device state.

### 1. Dispatcher 111

The application card contains the number, status, priority and transition history. You can supplement your own call with information about a threat to life, shooting, or a calm situation. The call can be canceled before arriving at the location; The crew that has already left completes the return. Canceling one call does not cancel the combined service call of another applicant. Queue priorities: casualties, life threat/OMON, ambulance/shooting, routine calls, patrol. The authorized officer sees the local control room; an ordinary citizen - his appeals.

Usage: telephone → calls → 111; then “City NChG” → “Dispatcher 111” → application card. Statuses show queuing, departure, arrival, crew collection, return and completion.

### 2. Cases IC and evidence

The interface includes automatic investigations and procedural cases of the existing authorities module. Each piece of evidence has a source, quality, custodian, and transmission history. Rain worsens open tracks; packaging stops further weather deterioration. The witness must see both the incident and the suspect; hidden script information about the killer is not shown as an established fact.

Independent readings are taken into account by source. Two independent witnesses or a witness together with a verified physical connection provide confirmation of the version. The mere presence of an item in inventory does not prove the commission of a crime. The seized item is first recorded as being in the detainee’s possession; connection with a specific crime requires separate confirmation. Inconsistencies prevent automatic confirmation. The news wording speaks of suspicion based on testimony, and not of proven guilt. There is no automatic verdict.

Usage: employee with appropriate authority → “City NChG” → “Cases IC”. The current sequence of investigation → prosecutor's office → court → execution of decisions is maintained.

### 3. Document verification, detention and seizure

During the inspection, you can ask for the employee’s identification and clarify the basis. The arrest creates a protocol with the date, employee, reason and further events. The contents during inspection and the actual seized items are reflected separately. Seizure requires authority, a person in custody, an open case, and a valid search warrant.

The item is actually transferred to the employee's inventory. Until confirmed by the engine, the recording remains pending; re-equipment does not create a second item. After landing and delivery, the status of the protocol changes. Delivery of NPCs by paddy wagon has been tested in the game.

In the menu “City NChG” after shooting, “Stop Resistance” is available. The character removes the weapon and must remain in place. Shooting, moving more than 6 m or changing the level cancels the surrender. The waiting period is 90 seconds. OMON gets the opportunity to accept the surrenderer and transfer the detention to the general procedure.

### 4. Transport register and towing

Purchased cars are registered automatically: owner, license plate, contract, access permissions, wanted/fine status. The owner can transfer the key, give power of attorney for 24 hours of active game time, revoke permissions, transfer property, report theft and report discovery. The transfer of ownership also changes the original transport contract. Access to the trunk and controls takes into account permission. Company cars and existing taxi services maintain their access procedures. Key - permission record; a separate physical key model has not been added.

Use: “City NChG” → “Transport Registry” by logging into State Services. To transfer, indicate the ID of a nearby recipient from the section’s contact list.

Towing: stop the KamAZ/Ural with its back to the front of the free vehicle, select it and secure the tow. Both machines are subject to opposing spring and damping forces; movement is not performed by teleportation. If the distance is excessive, the connection is broken. Uncoupling via the interface is available after both machines have stopped. The actual movement of a car and truck was tested at approximately 25 m.

A police officer near a found wanted empty car can issue a tow order. The order requires actual towing of at least 20 m and delivery to point IC. Payment is issued once; The car is transferred to the impound lot. Return to the owner costs 500. An autonomous NPC tow truck is not implemented in this stage: the tow truck is controlled by the player. The full evacuation route to the impound lot was not confirmed separately in the native run.

### 5. Infrastructure and engineering

Three logical nodes of the district infrastructure have been added to Dead City: design, power supply, communication. They use existing records of engineering assets; There are no new building models/shields. The service radius is 100 m. Zero power or communication functionality deprives the device of access to the network in the node area. Serviceable communication faults arise, and based on them, real repair orders appear.

Usage: “City NChG” → “Infrastructure”/“Work in the city”. For repairs, you need real materials and tools: components, wire/insulating tape; for electrical work - a multimeter and the necessary engineering skills. The materials are consumed, the condition of the node is restored. Payment is possible after actual completion and only once. The remuneration is fixed upon acceptance of the order and takes into account materials. This is local gaming infrastructure; There is no complete electrical diagram of the entire card and control of all static lamps.

### 6. Devices and account protection

Message/call histories and device settings are saved along with the world. Through another device of your own, you can declare the device lost, block it, and terminate your account sessions. Ownership, access to the control device and communication are checked. Blocking prevents access and resets the session and use in the botnet.

Usage: “City NChG” → “Device protection”. When blocked, a one-time recovery code is recorded in the notes of the control device. Unlocking is possible with the correct PIN or this code. The used code is destroyed. After physical unlocking, you can unmark the loss. Terminating sessions uses the authorization epoch: old sessions do not become valid after reopening the interface. You need to log in to State Services again.

### 7. City work

Orders appear from actual events: targeted delivery between living NPCs, node malfunction, damage to service vehicles, evacuation of a found vehicle. The package is a real unique item tied to the order. For issuance, receipt and payment, its actual owner is verified. Payment for delivery occurs after confirmation of receipt by the addressee, and not when a button is pressed. The death of the recipient blocks payment; return to sender/closure of impossible delivery is provided.

Usage: “City NChG” → “Work in the city.” Accept the order, look at the customer, place and conditions; use the target mark, then perform an action near the corresponding person or object. Active delivery is not duplicated. Cash payments are protected from re-draw and early termination.

### 8. Reputation

The opinion is kept separately by the witness, the district and the organization. The event is first known to a specific living witness; further spreads to the area and organization with delays and less weight. The death of a witness before transmission prevents distribution. Documented relationships with the customer/institution are taken into account separately. Performance and delinquency of bank debt affect the corresponding reputation.

A bad reputation can close city orders. Trading prices through the application take into account the attitude of a specific buyer within a coefficient of 0.85–1.15. The calculation of the displayed price and debiting money is general. All original Anomaly merchant prices are unchanged by this update.

## Diagnostics and installation

F7 → actions → “CCZMP: city diagnostics”: active requests, crews, reasons for delays, protocols, registry, input status and serialization. "CCZMP: Systems Master Snapshot" stores an independent copy of the state for comparison; further changes to the work log do not change the snapshot. Closing the window restores its own input capture.

Package and sources: `D:\CCZMP PROJECT\tools\city_systems_20261019`. `baseline/` contains the originals of the modified files, `baseline.json` - checksums, `installed.json` - installation log. `rollback.py` performs only checking by default; application - `--apply` when the game is closed. The installer refuses to change files when the game is running or extraneous changes are detected. Basic user saves and settings are protected by checksums.

## Checks

- Lua 5.1: 79 rules/integration adapter checks and 14 lifecycle checks; 93 in total. Compilation of all package scripts, XML and DDS has been checked.
- Native: restoration of correspondence after loading, blocking/unblocking and terminating sessions, interfaces of city sections, real transfer of a parcel with a deferred single payment, failure when the recipient is dead, complete repair of communication with the consumption of four components, F7 diagnostics and a control snapshot.
- Native: procedural case through the roles of IC/prosecutor's office/court, decisions, detention, actual transfer of the seized item, protection from re-seizure, boarding and delivery of NPCs by paddy wagon.
- Native: physical towing and detachment, about 25 m of movement of both cars.
- During a lengthy check, crash of conservation was discovered and localized: the standard `motivator_binder:save_state` was accessing the invalid `self.object` after clearing transportation participants. Added checking the client session generation by numeric ID, obtaining the current object from the level and early cancellation of callback at `net_destroy`. The retention of departed userdata and the forced deletion of engine records from runtime have been eliminated.

Repeat after correction: 23:09:16 - delivery of the detainee; 23:09:32 - deleting NPC and successfully saving `_cczmp_city_integrated_proof`. Files `.scoc` (1,036,743 bytes), `.scop`, and `.dds` have been created and verified. crash was previously played on this sequence. Repeated loading is checked by a separate run.
