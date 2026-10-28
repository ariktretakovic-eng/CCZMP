[Русский](../../../../snapshot-2026-10-28/05_%D0%9E%D1%80%D0%B3%D0%B0%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8_%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B_%D0%BC%D0%B8%D1%80/STATE_UNIFORMS.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# CCZMP - state chevrons and four ranks of special forces

Installed 10/09/2026 in D:\CCZMP PROJECT. Target game: Anomaly 1.5.1, offline.

## What's connected

The user's original chevron has been added to both shoulders of seven game models: state_soldier, state_duty, state_ecologist, spec01, spec02, spec03, spec04. The assignments cover all 13 organizations with type=state and five site employees - 18 profiles.

| Organizations | Model |
|---|---|
| MVD, MChS, OMON, IC, SChS, court, prosecutor's office, FSIN | state_soldier |
| Police | state_duty |
| Ministry of Health, scientists | state_ecologist |
| Alpha, Pennant | spec01–spec04 by organizational rank |

MVD/MChS/OMON and other departments at this stage are using their existing models in the project with a new chevron. New bodies from the “battery.rar” package are connected to Alpha and Vympel. The remaining GLTF donors remain material from the previous audit; their conversion is not included in this package.

## Ranks of the “Batteries” package

| Rank in menu | Internal index | Visual |
|---|---|---|
| 1 | 0 | actors\cczmp\state\spec01 |
| 2 | 1 | actors\cczmp\state\spec02 |
| 3 | 2 | actors\cczmp\state\spec03 |
| 4 | 3 | actors\cczmp\state\spec04 |

For Alpha and Pennant, four stages “Rank 1”–“Rank 4” have been added. This is CCZMP's organizational rank, not X-Ray's combat experience. New characters without the specified rank receive the first model. Existing NPCs retain their identity, inventory, documents, and job role.

Spawn: F7 → action section → CCZMP organizations → Alpha / Pennant → “Create employee - rank N.” Four buttons specify the selected organizational rank, which is saved with the NPC. For other organizations, the usual employee spawn remains.

When an NPC is promoted or demoted, the model is updated automatically within 1.5 seconds. During a conversation, the replacement is postponed until the end of the conversation. After loading of the old preservation, civil servants already at the level also receive a chevron. Regular NPCs outside of CCZMP government organizations are not affected. The player's model is determined by his equipment; changing organizational rank changes the NPC's appearance.

For scripts: cczmp_factions.set_object_rank(npc, 0..3); cczmp_native.spawn_member("alfa", 0..3) returns success, error and ID of the created NPC. Appearance settings: gamedata/configs/cczmp/agency_models.ltx. Appearance update: gamedata/scripts/cczmp_models.script.

## Geometry and textures

One additional material per model, two shoulder chevrons, approximately 8 x 10 cm. The geometry fits the sleeve and follows its bone weights. The chevron is oriented equally on both sides, without mirroring. Texture DDS DXT5 512 × 512, ten mipmap levels; the original PNG is saved separately.

The original body meshes, 47 bone order, IK, physics and animation references are stored in OGF byte by byte. Added a separate child mesh of chevrons. Standard game resources are not replaced globally.

## Checks

Re-importing all seven OGFs, loading DDS and applying standard walking - completed. LuaJIT's five integration tests check ranks, promotion/demotion, old persistence, ID reuse, spawn restrictions, and actual menu controller actions. 128 existing project tests have been passed.

The result of verification directly in X-Ray and cold boot is recorded in verification_result.json. Logs, shoulder renderings and test results are located in tools/agency_models_work/state_uniforms_20261009.

The package contains a ready-made gamedata folder for the current version of the project, the source chevron, build scripts and reports. Changed configurations and UI are based on the current CCZMP, so when moving to another branch they should be merged with its changes. The backup copy of the installed version is listed in backup.txt and contains the previous files.

The original archive “battery.rar” was provided by the user. There was no information about authorship or license in the archive; this package does not add permission to publicly distribute source models.

X-Ray verification has been completed: 19 employees of all 13 government organizations have been created; seven visuals were tested, promotion, demotion and cold loading with saved ranks. In the regular organization window, confirmation of the spawn of Alpha of the fourth rank was checked. The original 39 save files remain byte-by-byte unchanged; user.ltx settings have been restored; The temporary verification module has been removed.

? ???? ??????? ??????? ???????????? ?????????? ????? ????????????? ???? ????????????? motivator_binder: INCORRECT LOAD. ??????? ?? ??????????. ?????????? visual, ???????? ? ??????????????? ????? ???? 19 NPC??????????????? ?????????; ?????? ??????? ???? ?????????? ????????? AI-??????? ?? ??????????. ??? ?????????? ?????? ??????? ????????? ?????????? ??? ????????? ????????? ??????? ?????????. ??? ??????? ???????.
