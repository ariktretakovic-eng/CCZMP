[Русский](../../../../snapshot-2026-10-28/00_%D0%A2%D0%B5%D1%85%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5_%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%B0/OPERATIONS.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Organizational powers - offline, first implementation

In F6, the item “Powers of the organization” has appeared. The target is taken from the NPC at gunpoint before opening the window, or selected from the list of living NPCs nearby. To act with NPCs, a distance of up to 4 m is required. The player himself is available in the list of targets for applications and dossiers; Physical detention of a player is not supported by this module.

F7 → CCZMP → organization → join → “Select position (debug).” The position gives authority under the statute, but does not replace the requirements of a warrant, evidence, distance and state of the case. Added 15 court positions, 25 MVD, 10 Barricade levels. The names of the 7th–10th stages of the Barricade in technical specification are not completely specified: the interface designates them by number/approval.

## Testable working script

1. IC, position 2 and higher: select an NPC, open a case under the article, add a statement or record actual events. Position 3 and above: transfer to the prosecutor.
2. Prosecutor's office: open the register of cases and endorse the case for the court, or return it.
3. Court: select a case and issue an arrest or search warrant. For criminal cases, a District Judge is required (9); for administrative ones - Justice of the Peace (8). For protected officials, a Supreme Judge is required (15).
4. MVD (Corporal, 7) or other agency with the authority to: select an NPC and execute the arrest. The order is one-time only. For a search, open a corresponding file: a separate search warrant is required. The inventory contains real NPC items.
5. Trial: The statement alone does not prove guilt. The sentence requires an actual event related to the article or directly observable open carrying of a weapon according to Criminal Code 3.3. Acquittal closes the case, cancels active warrants, and releases the NPC.
6. FSIN: mark a prison point, escort the convicted person to it, place him in prison. The countdown begins upon placement. Upon expiration, the NPC is released automatically online. Pre-trial arrest ends after 24 game hours if there is no conviction.

To test several roles offline, you can change the organization via F7: the case, order and goal are saved. Authors of actions are recorded with the organization and position at the time of the action.

## Actions of existing organizations

- Court: warrants, verdict, acquittal, remand, release, removal for proven reasons.
- IC / SChS / police / MVD: cases, statements, observations, interrogation, transfer to the prosecutor; arrest/search based on a court warrant. SChS, police, MVD also convoy.
- Prosecutor's office: cases, materials, visa for court, return, removal.
- FSIN: warrant, convoy, prison registration, reception of a convicted person, release on time.
- OMON / Vympel / Alpha: execution of orders, convoy, release of hostages; Vympel/Alpha - security.
- All OCG: robbery, kidnapping, ransom, release of your own hostage. Barricade requires raid clearance 9 and prohibits kidnapping allies. The money is transferred from the actual NPC wallet. To threaten, you need a weapon in your hands or a wounded target. An actively resisting NPC does not linger.
- Zone of Power: illegal release of an arrested person; CorrSyndicate: bribery; Techno: theft/research of artifacts; Cobra/Spark/Sector0/Barricade: sabotage; Sector0: receiving PDA data; Fanatics: Research.
- ZonaStroy / ChernEnergo / Komnet: construction/repair of a registered node, power supply, communications. These are the saved indicators of the object; visual buildings, the map's power network, and physical radio communications are not yet created.
- Service station Kanban: repair of items with consumables, delivery. Subbers: sound pulse at 15 m, delivery. Operators: delivery, support.
- PMC / Snipers: security and escort; Stalkers: research, delivery, escort.
- MChS: treatment, hostage rescue, unit repair, escort. Ministry of Health: treatment, radiation removal, medical record. Scientists: research and treatment.
- Killers: contract for a real hostile target of the customer, collateral from the customer’s money, payment for a confirmed kill by the player.
- Civil: complaint, item delivery, medical record.

Consumables, distances and times are set in gamedata/configs/cczmp/operations.ltx. Treatment/repair changes the actual health and condition of items. Transfer, theft and research work with real inventory. Services do not create a monetary reward out of thin air.

## Limitations of this stage

Physical detention/convoy changes the default logic of only regular simulation NPCs (sim_*), so as not to destroy the scripts of story characters. Legality is checked by the module, not by the interface button. This is an offline execution of actions by the player; offline investigators, NPC court sessions, jail cells/routes, and online server have not yet been implemented.

Qualification and sentence are selected according to the current LTX Criminal Code/Administrative Code/FP; the robbery is recorded as a fact without a fictional article. In the F6 menu, the sentence uses the lower limit of the range; the NPC court reception office offers the calculation and selection of the border provided for in the article with a separate confirmation (see CIVIC.md); a full review of the sentence with the return of the fine, repetition of NPC sentences, property claims of FP4 and an additional judicial procedure are not yet available. The appeal is disabled in the powers until the reversal of the consequences of the verdict is implemented. Organizations that are not yet in the registry 34 are not added at this stage.

The status of cases, warrants, arrests, files and services is stored in alife_storage_manager; terms - in standard CTime. Missing/dead/replaced NPCs are re-checked. Combat events do not automatically cause condemnation.


## Agency pilot, 2026-10-08
Real SK/prosecutor/judge/MVD/FSIN employees, bounded NPC authority context, patrol custody and native AI escort are implemented for l05_bar. See [CIVIC.md](../05_Organizations_Documents_World/CIVIC.md) for controls and limits. Legal NPC identities now persist in ALife server storage. Warfare custom-community squad buckets are initialized safely; this does not add territorial agency spawning.
