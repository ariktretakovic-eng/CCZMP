[Русский](../../../../snapshot-2026-10-28/05_%D0%9E%D1%80%D0%B3%D0%B0%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8_%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B_%D0%BC%D0%B8%D1%80/CIVIC.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# CCZMP: departmental pilot site

Offline, Anomaly 1.5.1. Map “Bar/Rostock” (`l05_bar`), courtyard near the fire, coordinates approximately X=200, Z=110. This is a temporary placement for mechanical testing; courthouses and IC in Pripyat remain the next stage.

## Employees and entrance

On the first visit to the area, one investigator IC, a prosecutor, a judge, a patrolman MVD and an inspector FSIN are created. Repeated loading does not create duplicates. Dead employees are not automatically revived.

Approach the employee and start a normal conversation: “Contact a work issue.” The reception area uses a terminal window. F6 also has "Departments in the game world" with a list of employees and distances. The judge marks the area on the map.

## Case → warrant → detention

1. From the investigator, select a present NPC and an article, make a statement. You can work with a previously created case from F6.
2. The investigator adds verified observations and transfers the case to the prosecutor. The statement in itself is not sufficient evidence for a conviction.
3. The prosecutor confirms the materials or returns the case.
4. The judge issues separate arrest and search warrants and makes a decision on the case at the request of the player. There are no automatic sentences.
5. The patrol checks active orders for nearby ordinary `sim_` NPCs, approaches the target and detains it if there is no resistance.
6. The detainee goes to point FSIN along the standard AI grid, the patrol accompanies him. When a convoy is lost / a battle begins / a timeout occurs, the normal hold returns.
7. Without a sentence, this is pre-trial detention with the existing limit of 24 game hours. After the verdict, FSIN receives a nearby detainee and starts the sentence. The prison item previously selected via F6 is not automatically replaced.

## Documents and saving

The “Check against official registry” button is available in the passport/ID when the player is allowed to read the dossier. The registry shows cases, active warrants and the arrest of the document holder. The possibility of arrest further verifies position and distance. A stolen document retains a connection with its original owner.

The NPC's identity, organization, and position are now stored in the ALife server state and survive going offline. Existing old format online records are being migrated. Connections already lost by older versions are not re-linked to new NPCs using the same name.

Documents FSIN reflect the position of inspector. The current registry technical specification for the prosecutor's office and FSIN do not have a rank scale; numerical ranks are not invented for them. IC, court and MVD use their actual position/rank tables.

## Pilot Limits

- The patrol operates in the area of the site: searches for targets within 35 m from itself and 50 m from the base. The player and story NPCs are excluded from automatic detention.
- Employees remain normal vulnerable NPCs. Hostilities and fights block the reception and execution of the police scenario; The player's reputation is not reset.
- The containment facility is still open, without a separate building, locked doors and cells. Standard NPC models are used; new forms and interiors have not been created.
- The investigator and the court work on requests through dialogue. There is no independent investigation of all the crimes of the world.
- The offline convoy is suspended when moving to another map, the state of detention is maintained.

Backup: `_backups/civic_20261008`. Test results and individual test saves: `tools/civic_work`.


## Verification, 2026-10-08
110 regression tests passed. A private neutral-reputation save completed the real X-Ray case -> prosecutor -> warrant -> patrol arrest -> escort -> FSIN sentence scenario. Cold restart retained prisoner age 48, document UID 63, person p60, case 62, the executed warrant, sentence and five staff without online duplicates. Passport registry callback opened the correct owner record. Final initial and reload engine logs contain no FATAL ERROR; earlier failed runs are archived separately. Existing hostile player reputation was changed only in the private fixture. All 36 original user-save files retain their SHA256 hashes. Test scripts were removed from gamedata.


## Judicial reception: calculation and confirmation

Open the case with the judge that the prosecutor submitted to the court. If there is verified evidence, “Make a verdict” will appear; this opens the preliminary calculation and does not apply the penalty yet. Statements by themselves are not considered such evidence.

The calculation shows the term, fine and additional sanctions of the article. If the article specifies a range (currently Criminal Code 9.1 is from 1 to 5 years), select the lower, middle or upper limit. Articles with a fixed punishment do not propose changing it. The conversion of years to game days remains specified by the existing law config.

Select Confirm Conviction, then click OK. The backend re-checks the judge's credentials, the stage of the case, the evidence, and the identity of the target. A closed case cannot be re-convicted through the old window. “Back” only cancels viewing the calculation; NPC money and wealth do not change.

An existing warrant can be canceled from the case file of a judge with sufficient position. Executed and previously canceled orders do not have this button. The articles are deciphered on the cards; actions of the investigation, prosecutor's office and court are shown according to the stage of the case. For FSIN, the prisoner card displays the assigned sentence and the remaining game time.

This feature applies to the reception NPC. The old sentence action in the F6 menu retains the lower bound. Appeal and automatic investigation were not added by this change. Backup: `_backups/civic_court_20261008`.
