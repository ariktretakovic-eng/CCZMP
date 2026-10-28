[Русский](../../../../snapshot-2026-10-28/03_%D0%9F%D1%80%D0%B5%D0%B4%D0%BC%D0%B5%D1%82%D1%8B_%D0%B3%D0%B0%D0%B4%D0%B6%D0%B5%D1%82%D1%8B_%D0%BC%D0%B5%D1%85%D0%B0%D0%BD%D0%B8%D0%BA%D0%B8/__README_RU.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# CCZMP: trunks, gadget screens and help

Update to existing project Anomaly 1.5.1, October 10, 2026. This is an addition to the previous CCZMP build; it uses already installed items, documents, transportation, banking and hacking. No new game required. Models and executables are not changed.

## Installation and rollback

Copy the `gamedata` folder over the current build when the game is closed. On the working PC, the update is already installed in `D:\CCZMP PROJECT`. The checks are in `tools/tests`; they do not need to be launched for normal play.

Backup copy of the replaced files on the working PC: `D:\CCZMP PROJECT\_backups\trunk_devices_20261010_135834`. Its `manifest.json` lists the paths and initial checksums. When rolling back, restore files with non-zero `old` and delete added files with `old: null`. Before rolling back, load a save made before using the new trunks: the previous build does not provide access to their contents.

## Trunk

1. Approach the rear of the car from the outside. Press **F** when pointing at a car.
2. On the left are the car’s things, on the right are the player’s things. Transfer by double clicking or dragging between sides. There are no buying or selling baskets.
3. Close with the button or **Esc**. Make a save after the transfer to consolidate the state.

Each machine has its own storage. A common processor for standard vehicles is used, including CCZMP vehicles. The doors/cabin maintain normal interaction with the vehicle. The trunk that is locked with an alarm is inaccessible. It cannot be opened from the interior. First put worn and active items in your backpack; quest items do not fit in the trunk. A rented car with things in the trunk cannot be returned.

The original objects are transferred rather than copies are created. The content belongs to the game save: after a complete restart and loading save after transfer, it remains in the machine. loading saving before transfer returns the entire world to that moment, including objects in the same place. Changes without subsequent saving do not survive loading of the old file.

Technically, real items change the ALife parent to a hidden container associated with a specific car by ID, name and section. A record of the container and pending transfer is saved with the machine. A repeated request does not duplicate the transmission. If a container is lost, the system does not recreate its contents. The item's state is restored from the record on first access after loading; the gadget/document data remains on the original server object.

The weight limit of the trunk, the animation of the lid, or the removal of cargo from a car completely removed from the world have not been added. The machine's transition between cards is provided by moving the container; A separate game run of such a transition has not yet been completed.

## Gadgets

Open the device through its action in the inventory or select the device in the items section of the **F6** menu. Phones PDA and PDA get a vertical screen; tablets, laptops and PCs - wide. Design and applications vary by OS.

| Application | Destination |
|---|---|
| Bank | Existing CCZMP Banking Services |
| Map | Standard card in PDA |
| News | Gaming news |
| Magazine | Existing Event/Transaction Log |
| Settings | Charge, installed OS and device actions |
| Contacts, Messages | Telephone functions; available on phones |
| Hacking | Already implemented operations and their limitations |
| Registry | Service OS; existing authority checks |
| Terminal | Game Services Teams |

Applications access legacy services; charge, SIM, device lock, interference, organization rights and tool requirements continue to be checked where required. The mere appearance of an icon does not provide access to protected operations.

Terminal commands:

| Team | Action |
|---|---|
| `help`, `status`, `apps` | Help, device status, application list |
| `open bank`, `open settings`, etc. | Open the application by ID from `apps` |
| `clear`, `home` | Clear history / return to home screen |
| `recharge` | Charge through existing battery consumption |
| `os`, `os <имя>` | List of installed OS / switching |
| `hacks` | List of available operation names |
| `target`, `target <ключ>` | Check selected target / set character key |
| `run <операция>` | Run the operation with the same checks |
| `job`, `cancel` | Active operation status / cancel |

**Enter** executes the command, **Esc** closes the screen. This is the terminal of the gaming device; It does not execute Windows system commands. The new shell does not add non-existent applications, the Internet or new banking/hacking logic.

## Help, licenses and recipes

Certificate IC, category A/B/C/D licenses and medical prescription are supported. Open with the action of an item in the inventory. The form shows the name, coat of arms NChG, number, recipient, organization, full name and position of the issuer, game date and time of issue, content and status. For a prescription, the medication and doses used are also shown.

Issue through a character records his actual name and position at the time of issue. When issued via debug, a random name and position of a suitable department is created. This information is recorded once and does not change when you open it again or loading.

For a valid permit in **F7**, use the special action of issuing a certificate/license. Direct spawn of a form from the catalog creates an item, but does not itself register legal clearance - this is noted in the view. The recall and expiration date of the prescription are reflected in the status. Old documents without a historical date/position are shown “not specified”, without retroactive invention. The known name of the old physician/issuer is retained.

## Voice acting: preparation, without ready-made recordings

82 texts have been prepared: a greeting and a remark when showing a document for 41 organizations, see `voice/voice_lines.json`. The Russian speech generator failed with HTTP 403; There are no ready-made voice files in the update. Original Anomaly replicas are not used as replacements.

Connecting your own records: `gamedata/sounds/cczmp/voices/<код организации>/document.ogg`. The processor reproduces this replica when showing a document/certificate from the relevant department; without a file there is silence. X-Ray compatible mono OGG Vorbis is recommended.

For greetings, there is a call `cczmp_voice.play(organisation, "greeting")` and a file `greeting.ogg`, but automatic replacement of all NPC conversations is not yet enabled. This small set of lines is not a complete re-voicing of all the dialogues.

## Validation and boundaries

Regression tests were performed under Lua 5.1: 276 different tests of existing and new systems. After the last changes, 43 interface/document checks and 51 item checks were repeated. In the game run, the transfer of the original item, opening the trunk through the standard use handler, six gadget screens and terminal commands, help, returning to inventory and F6 are checked. Separate restarts check the status of saves before/after transfer and protection against re-extraction.

A native trunk check was performed on a Niva; connection of other cars is based on a common standard binder and checks for determining the rear zone. This is not a statement about a full play test of each donor model.

One intermediate game run ended with a native crash without a Lua error; After correcting the markup and texture states, the second full run was completed. The exact cause of that intermediate failure has not been determined. In additional runs, an erroneous test requirement for the total number of things was discovered: in the interactive window, additional cartridges entered the trunk. This is a separate original object, not a copy of the component. The test has been specified: it checks the selected object and the safety of the others. Intermediate images with a black bottom edge were taken when the size of the game window and the remote display did not match. The final help and terminal were tested entirely at 1440x900; other permissions were not tested separately.

The archive does not contain test saves, automatic running of the test script, speech generator dependencies, or user data. Confirmation logs are in `verification`.
