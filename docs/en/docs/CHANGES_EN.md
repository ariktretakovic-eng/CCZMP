[Русский](../../CHANGES_RU.md) · **English** · [Documentation index](INDEX.md) · [Translation notes](../TRANSLATION.md)

# Updating documentation

## 10/29/2026

Navigation is synchronized with the published composition of the repository and more recent Autonomous Life V1 and CCZMP Locks materials. The original reports from previous stages have been saved.

| Clarification | Source | How to read now |
|---|---|---|
| Early Pilot 3 NPCs → minimum core for 22 existing villagers | [Report V1](snapshot-2026-10-28/13_Autonomous_Life_V1/REPORT_EN.md) | Partially implemented; full V1 and the entire population are not accepted |
| Work, food, real postings and vacancies | [Native tests](snapshot-2026-10-28/13_Autonomous_Life_V1/TEST_REPORT.md), [contracts](snapshot-2026-10-28/13_Autonomous_Life_V1/API_CONTRACTS.md) | You cannot transfer the old “food is not consumed” to the new kernel |
| Warm loading | [WARM_LOAD](snapshot-2026-10-28/13_Autonomous_Life_V1/WARM_LOAD.md) | Primary crash, then two normal successful repeats; extended transition not accepted, C++ AV reason not established |
| Locks and PIN cases published with test bench | [Module](../modules/cczmp-locks/README.md), [protocol](../modules/cczmp-locks/TEST_REPORT.md) | Sources of stage 09.10, repeated 21/21 mock tests on 29.10; this is not a new native run of the entire game |
| Old root INDEX from 02.10 | [Archive](archive/INDEX-legacy-2026-10-02.md), [new index](../INDEX.md) | Old file/link counts refer to historical local installation |
| Navigation and composition of the publication | [Document Index](INDEX.md), [FILES.json](../../FILES.json) | The list is built from Git files; it does not describe the hidden working gamedata |

The transport summary retains 85 sections from the 10/28 audit; There is no new confirmation of the full readiness of each machine. The numbers 41 organizations, 197 product records and 51 application records also relate to audit rather than general acceptance.

Not closed: full save/UI regression, explanation of access violation, behavior of all citizens nearby, families and housing, full GOAP, supply, large industrial economy, individual acceptance testing transport and network mode. Priorities and criteria are in the [road map](ROADMAP_EN.md).

Updating documentation checks the composition, references, and consistency of summaries. The gaming tests described in the original reports were not re-run for this publication.

## English edition — October 29, 2026

Added English counterparts for all 87 documentation files, including historical `.ltx` concepts, short `.txt` notes, the archived index and module guides. Russian originals remain available. Both indexes connect the language versions. `tools/check_docs_translations.py` checks coverage, structure and preserved technical examples. Game source code and in-game localization are unchanged. Translation used machine assistance; entry pages were edited. See the [translation notes](../TRANSLATION.md).
