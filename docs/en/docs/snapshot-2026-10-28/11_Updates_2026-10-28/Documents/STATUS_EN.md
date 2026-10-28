[Русский](../../../../../snapshot-2026-10-28/11_%D0%9E%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F_2026-10-28/%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B/STATUS_RU.md) · **English** · [Documentation index](../../../INDEX.md) · [Translation notes](../../../../TRANSLATION.md)

# CCZMP - donors, package October 22, 2026

## Status
- Working game: `D:\CCZMP PROJECT\gamedata`.
- Sources: `D:\CCZMP PROJECT\tools\доноры`.
- Audit: 239 archives and single 3D sources, 210 exact comparisons with previous registries, 24 new archives from October 18–22, as well as 5 previously taken into account sources.
- 24 new archives yielded 25 separate OGF models: the sedan/wagon car kit is divided into two models.
- Installed **583 files** (OGF, DDS, XML, LTX, Lua) with hash checking; 25/25 OGF passed the texture accessibility test.
- Backup: `D:\CCZMP PROJECT\_backups\donor_import_20261022_234140`.
- Manifests: `tools\donor_import_20261022\installed.json`, `baseline.json`, `expected_sources.json`.

## Models and game classes
- `cczmp_fv_222..237` - civilian cars, bus, truck, EBRC Jaguar, including two sedan/wagon versions (`230`, `246`).
- `cczmp_fa_238` Ka-52; `cczmp_fa_239` Su-30MKK; `cczmp_fa_240` Su-27SK.
- `cczmp_fworld_241` Liebherr tower crane; `cczmp_fworld_245` Goldeneye Dam.
- `cczmp_fv_242..244` — official police cars; `cczmp_fv_246` is a separate second body made of lowpoly sedan/wagon.
- All new sources are kept unchanged. Textures were prepared taking into account the OGF binding, the encoding of game text files is Win-1251.
- Automotive sections use X-Ray automotive class and the general W140 physics framework, with customization of model, weight, wheel joints, fuel parameters and issuance rights.
- Aviation sections use a game holder and a physical prototype of the Mi-2; Individual parameters for speed, climb and flow rate have been created. They do not yet have full-fledged aircraft aerodynamics, animated Ka-52 rotors, proven flight and all cockpits.
- The crane and Dam object are integrated as separate world OGFs, **not** as a full-fledged crane and not as a new location with AI navigation.

## Game test (separate profile)
- Profile: `tools\donor_import_20261022\native_appdata`.
- AnomalyDX9AVX is running, location Dead City is loaded: WORLD_READY/PRIVATE_READY.
- All 25 new sections: `system_ini():section_exist(section) == true`, 25/25.
- `cczmp_fv_242`: physical spawn and CCar confirmed, engine available, health=1, fuel=70.
- `cczmp_fv_230`: physics spawn and physics shell confirmed.
- `cczmp_fv_226`, `cczmp_fa_238`, `cczmp_fa_239`: placement answered `no_place` in the test part of Dead City; should not be considered a full ride/flight test.
- Save `_cczmp_import22_physical` was successfully created in private profile (.scoc, .scop, .dds).
- When loading was saved via the console in the same process, `0xC0000005` (access violation), dump `native_appdata\logs\xray_user_10-22-26_23-50-06.mdmp` was observed; Suspected to be a net_spawn/userdata clearing issue, cause undetermined. The separate save run test is performed separately; until its result, persistence is NOT confirmed.

## What has not yet been confirmed
- driving tests and steering control of each car.
- Flight of the Ka-52, Su-27 and Su-30 (only prepared aircraft prototypes).
- Passenger movement/bus interior.
- Special works of crane, forestry machines, Tor-M1 and old trains, independent aircraft aerodynamics of Rafale.
- Correct textures and collisions of all 25 new models in different DX renders.
- Full cycle of saving → ending the game → loading after installation.

## Rollback
When the game is closed, do:
`C:\Python314\python.exe "D:\CCZMP PROJECT\tools\donor_import_20261022\rollback.py"`
— check the possibility; add `--apply` only when you need to restore previous files. The rollback stops when it detects files modified by third-party code and does not affect saves or user settings.

## Attention
New donors have been added with prototype functionality by type, but this **does not mean** that all unique special mechanisms, accurate physics and game tests have already been completed. The transport routes of organizations in this package did not change.
