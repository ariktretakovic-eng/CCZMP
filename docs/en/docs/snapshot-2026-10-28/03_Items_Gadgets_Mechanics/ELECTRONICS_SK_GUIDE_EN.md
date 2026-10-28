[Русский](../../../../snapshot-2026-10-28/03_%D0%9F%D1%80%D0%B5%D0%B4%D0%BC%D0%B5%D1%82%D1%8B_%D0%B3%D0%B0%D0%B4%D0%B6%D0%B5%D1%82%D1%8B_%D0%BC%D0%B5%D1%85%D0%B0%D0%BD%D0%B8%D0%BA%D0%B8/ELECTRONICS_SK_GUIDE_RU.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Electronics and trips IC - STALKER X CCZMP

Version: October 15, 2026. Mechanics work inside the game world of Anomaly 1.5.1.

## How to start

1. Buy a gadget from a suitable merchant or use F7 → CCZMP → items. Existing device sections are retained.
2. In the inventory, right-click on the gadget → “Open”. Ordinary phone, PDA and PDA start without a terminal.
3. The phone needs a SIM and a tariff for the network. Install SIM from Settings having `cczmp_sim_module` then select Basic or PRO. PDA, tablets and computers have a built-in network module.
4. In the store, select the application and confirm installation. The search is entered into the line below; then select Find. On the desktop, the Home button switches the icon pages.
5. The list contains action lines and explanations. Select the desired action, enter a value if necessary, then Confirm. Esc closes the device. Home and Back do not delete data.
6. Charging requires `cczmp_battery_device`; desktop PC needs `cczmp_power_module`.

## Persistent data

The data belongs to the physical UID of the item: applications, correspondence, contacts, calls and responses in a conversation, files, notes, tasks, owner session and settings. Rearranging an item does not create a clean copy. Saving the game saves this data; an earlier save returns them to their previous state. Old available SMS are transferred once; Records previously deleted by the restriction of the old version cannot be restored.

Font, scale, wallpaper, and color settings are stored in the OS profile of that device. Background tasks consume battery power and run during active gaming, including when the gadget is open. Pausing and exiting the game stops these tasks. Interest on banking products uses existing gaming time, including sleep.

## Communication

Contacts can be found from NPCs within a radius of 150 m and saved by number. SMS: `+7000номер текст`. The call log stores the result and duration. Text questions about location, help and news are available. Some regular NPCs receive a phone; senior civil servants receive a protected apparatus. The number and previous account are retained after the phone is removed.

## Shops and terminal

The official store is available on all gadgets; incompatible programs are filtered out. The terminal is free and can be installed on any type of device. Specialist devices and hacker models have it natively.

Open `freedom-zonedroid.nchg` in a specialist browser → download `F-zondroid.apk` → select “Install F-zondroid.apk”. F-Zondroid programs do not appear in the official store. Firefox Private Edition, Nmap, Zenmap, Wireshark, mitmproxy and Hydra are available pre-installed on Kali Linux laptops/PCs.

Example commands:

```
help
status
apps
sudo apt update
sudo apt install tor-browser john botnet
nmap gosuslugi.nchg
hydra gosuslugi.nchg
job
exfil gosuslugi.nchg
ls
tor on
sell 123
john 456
bot 456
ddos weather.nchg
ddos stop
```

`123` is the UID of the file from `ls`, `456` is the UID of the available physical device. The UID is visible in DeviceCare. To decrypt and install the agent, the original device must be in your inventory. Local decryption does not require a network. `cancel` stops the task, `cat UID` reads the file, `rm UID` deletes it, `echo текст > имя.txt` creates the file.

All addresses and tools work only with the `.nchg` virtual network. Services have capacity, protection, ports, version and log. The scan reports their actual condition; Hydra requires a preliminary scan and is limited after a series of attempts. A protected NBZ cannot be opened with the same weak password that worked on the test weather server. Uploading the register contains citizens registered in the current world and the fines assigned. There is no charge for reselling the same set.

The botnet uses individual captured devices: charge, power, connection and SIM affect the availability of the node. The load is limited in time, which actually reduces the availability of the game service. Removing the agent via DeviceCare eliminates the node. The security update revokes old access. Tor/VPN changes the visible source of traffic, but does not delete banking history.

## Public services and NBZ

Public services show the identity and affairs of the owner of the active session. NBZ uses the same citizen key. The player's cash and account balance are separated: first deposit money through the NBZ. Translation: recipient key and positive integer amount, for example `actor 1000`.

Someone else's unlocked device retains the owner's session. The transfer, deposit and credit from this session change exactly his account and obligations. “Login to your own account” only switches the session, it does not overwrite the physical owner of the item. All transactions leave records. Restrictions and conditions of banking products are taken from existing NBZ configs. When an NPC's personal account is first created, they receive a portion of their cash; money is transferred rather than created additionally.

## Murder and investigation

The exit is triggered by a living witness who was within 70 m and saw what was happening; criminal organizations do not report. Cases nearby within the first minute are combined. Within a minute of active play, the testimony is recorded: if the eyewitnesses who saw the face died before the testimony was transmitted, the killer remains unknown. A mask/helmet makes it difficult to identify a person. The death of a witness after recording does not erase the transmitted testimony.

At a busy location, the group travels along an existing surveyed road route in a separate W140_SK. Three employees are visible inside; behind them are three permanent NPCs. Two guard the place, the third approaches the body and examines it. Up to two groups per location; machines and employees are reused. If the road is blocked, there is no fuel, a body is unavailable, or the crew is lost, the case is delayed instead of automatically completing successfully.

The passport or ID must actually be with the deceased and relate to him: then the inspection takes 10 seconds. Without them - 60 seconds and identification is possible using a living colleague-witness. Removing documents before inspection makes identification difficult; once the identity is registered, it does not erase the file. Found documents and devices are transferred to the investigator's inventory and recorded as physical case materials. News publishes only established information, once per case. Witness suspicion in itself is not an automatic verdict.

Government applications require character credentials. The investigative interface shows cases and collected materials. The group can detain available regular NPCs based on a recent incident recorded; The player is asked to stop. Full forced confinement of the player and trial require a separate development of the existing punishment system.

## Catalog

The cost below is the installation price, not the device price. `phone` - phone, `pda` - PDA/PDA, `kpk` - simple PDA, `tablet` - tablet, `laptop` - laptop, `pc` - computer. `all` - all types. Alternative programs additionally require a specialist class. The utility software's credentials are checked.

| Program/ID | Channel | Types | RUB | MB |
|---|---|---|---:|---:|
| ZonMaps Pro / `maps` | official | all | 0 | 120 |
| StalkerCalc/`calc` | official | all | 0 | 4 |
| ZonRadio / `radio` | official | all | 0 | 12 |
| ArteFinder / `artefacts` | official | pda,kpk,tablet,laptop,pc | 500 | 30 |
| FactionChat / `chat` | official | all | 0 | 18 |
| WeatherZone/`weather` | official | all | 0 | 12 |
| MedHelper/`medhelp` | official | all | 200 | 40 |
| BattleLog/`battle` | official | pda,kpk,tablet,laptop,pc | 0 | 15 |
| TradePad / `trade` | official | all | 0 | 25 |
| ZonCamera / `camera` | official | all | 0 | 25 |
| CryptoPDA / `crypto` | official | all | 1000 | 35 |
| FoodTracker / `food` | official | all | 0 | 8 |
| StalkerDB/`database` | official | all | 0 | 80 |
| ZonNews+ / `news` | official | all | 0 | 10 |
| TacticalMap/`tactical` | official | pda,kpk,tablet,laptop,pc | 800 | 60 |
| RepChecker/`reputation` | official | all | 0 | 10 |
| ArmorCalc/`armor` | official | all | 300 | 15 |
| ZonTranslate/`translate` | official | all | 0 | 20 |
| ZonTerminal / `terminal` | official | all | 0 | 15 |
| NBZ - National Bank of the Zone / `bank` | official | all | 0 | 25 |
| Public services NChG / `government` | official | all | 0 | 25 |
| TaxiLink / `taxi` | official | all | 0 | 18 |
| JobHub/`jobs` | official | all | 0 | 15 |
| DocReader/`reader` | official | all | 0 | 10 |
| BackupLink/`backup` | official | all | 0 | 20 |
| DeviceCare / `care` | official | all | 0 | 8 |
| EngiDesk/`engineering` | official | pda,kpk,tablet,laptop,pc | 500 | 80 |
| CircuitLab/`circuits` | official | tablet,laptop,pc | 500 | 120 |
| FieldMeasure/`measure` | official | pda,kpk,tablet,laptop,pc | 300 | 30 |
| VehicleLink/`vehicle` | official | pda,kpk,tablet,laptop,pc | 500 | 50 |
| Service registry / `registry` | official | pda,kpk,tablet,laptop,pc | 0 | 50 |
| EvidenceDesk / `evidence` | official | pda,kpk,tablet,laptop,pc | 0 | 80 |
| MedStation / `medical` | official | pda,kpk,tablet,laptop,pc | 0 | 80 |
| Dispatcher / `dispatch` | official | pda,kpk,tablet,laptop,pc | 0 | 50 |
| NetScope/`netscope` | official | all | 0 | 25 |
| CipherLab / `cipher` | freedom | pda,kpk,tablet,laptop,pc,phone | 1000 | 90 |
| DataRecovery/`recovery` | freedom | pda,tablet,laptop,pc | 800 | 100 |
| RadioLab / `radiolab` | freedom | pda,kpk,tablet,laptop,pc | 500 | 80 |
| F-Zondroid / `freedom` | website | all | 0 | 15 |
| Firefox Private Edition / `firefox` | freedom | all | 0 | 180 |
| Nmap/`nmap` | freedom | all | 0 | 35 |
| Zenmap/`zenmap` | freedom | tablet,laptop,pc | 0 | 45 |
| Wireshark/`wireshark` | freedom | all | 0 | 130 |
| mitmproxy/`mitmproxy` | freedom | all | 0 | 80 |
| Hydra/`hydra` | freedom | all | 0 | 40 |
| John/`john` | freedom | all | 0 | 70 |
| Hashcat/`hashcat` | freedom | all | 0 | 200 |
| Tor Browser / `tor` | freedom | all | 0 | 180 |
| VPN Client / `vpn` | freedom | all | 0 | 25 |
| Network console / `botnet` | freedom | all | 0 | 50 |

## Technical files

- `gamedata/scripts/cczmp_electronics.script`: UID, OS profiles, power, rights and device data.
- `cczmp_app_catalog.script`, `cczmp_electronics_ui.script`, `cczmp_gadgets.script`: directory, application actions and interface.
- `cczmp_comms.script`: numbers, tariffs, message delivery and calls.
- `cczmp_netchg.script`: services, access, logs, tasks, datasets and game nodes.
- `cczmp_bank.script`: accounts, transfers, deposits and loans with owner context.
- `cczmp_investigations.script`: witnesses, crews, inspection, materials and news.
- `gamedata/configs/cczmp/investigations.ltx`: navigation and animation of employees.
- `gamedata/meshes/cczmp/vehicles/sk/mercedes_sk_crew.ogf`: separate crew model. The original W140_SK has been saved.

A backup copy of the source files and reports are located in `tools/electronics_sk_20261015`. Test saves are separate from the user profile. A new game is not required; Before using new mechanics, a separate save slot is recommended for convenient comparison.
