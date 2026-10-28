[Русский](../../../../snapshot-2026-10-28/05_%D0%9E%D1%80%D0%B3%D0%B0%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8_%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B_%D0%BC%D0%B8%D1%80/DOCUMENTS.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Passports and IDs CCZMP

Installed in the offline version of Anomaly 1.5.1.

## How to open

- In a normal conversation, a player from a law enforcement agency can use the remark “Demand to show documents.” She opens her interlocutor's passport.
- When talking with an employee of a law enforcement agency, the remark “Show your official identification” is available.
- If documents are checked by an employee of a law enforcement agency, the button at the bottom allows you to switch between the passport and the current ID of the interlocutor.
- Own item in inventory: context menu → “View document”. Closing: Close button or Esc.

The list of power organizations is located in gamedata/configs/cczmp/documents.ltx:
police, MVD, FSIN, SChS, IC, OMON, Vympel, Alpha, army.
The player's actual organization is used, including disguise checks.

## Data

Identity is stored in the NPC's world and server object data, so the age, name, and number are retained after talking again, the NPC going offline, and saving/loading the game. Age is assigned once, from 18 to 65 years. In existing saves, an entry is created when the character first appears online; a new registry is created in a new game.

The photo is taken from the character_icon() of the NPC profile. For the type name "Ivan Petrov" profile data is used. If the profile contains “Private Petrov”, the last name is retained, the first name is assigned once; the title from the profile name does not fall into the name field. For one call sign, a constant first and last name are assigned, and the call sign is shown separately.

The certificate shows the current organization and position from the CCZMP rank system. NPC combat rank does not replace organizational position. Upon dismissal, the certificate is marked as invalid.

Documents are issued to online characters gradually. The owner is issued one passport and one certificate upon joining a security organization. A lost document is not automatically reissued. Transferring an item to another character does not change its owner on the document.

## Resources

Passport and ID are separate items with new geometry, textures and icons:
gamedata/meshes/cczmp/documents/
gamedata/textures/cczmp/documents/
gamedata/textures/ui/cczmp_documents_items.dds

The interior uses the provided State Department seal, coat of arms NChG and flag. The person's photo is filled in by the game interface while viewing.

Editable X-Ray models: tools/document_models/*.object.
Generator: tools/build_cczmp_documents_assets.py; skeleton metadata: tools/documents_reference.json.
The generator requires Python and Pillow with DDS/DXT5 support. If the source JPEGs are not in tools/document_sources, the generator uses the saved DDS of coats of arms and flag.

New dialogues have been added to 1816 NPC profiles. For NPCs with whom the engine prohibits conversation, dialogue is not created. When you subsequently replace character_desc*.xml with another mod, you must save actor_dialog cczmp_demand_documents and cczmp_request_credential.

## Checks and backup

Tests: python -m unittest discover -s tools/tests -v.
Check log, test results, source files and saves:
_backups/documents_20261007_235658/

The temporary verification script zz_cczmp_documents_check.script is deleted after verification. Production scripts do not switch the player's organization or automatically end the game.


## Legal registry link, 2026-10-08
Passport/service ID records retain the owner person_key. Authorized players can open the owner registry from the document window, including documents held by another character. Persistent ALife storage retains age, identity, organization and job across offline transitions. See [CIVIC.md](CIVIC.md).

Correction of document input 10/08/2026: buttons are registered along with the names of the handlers; The close button and Esc hide the window and unregister it. The transition to the registry occurs after the click is completed. In X-Ray, page switching, closing, registry, F6/F7, passport from inventory, item properties, food use, and normal dialogue of an escorted NPC without a squad were tested. Completed 128 Lua 5.1 tests and 8 LuaJIT regressions. Logs: tools/ui_fix_work. Temporary game test scripts have been removed; the original saves are not modified.
