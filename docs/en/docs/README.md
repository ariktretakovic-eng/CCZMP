[Русский](../../README.md) · **English** · [Documentation index](INDEX.md) · [Translation notes](../TRANSLATION.md)

# STALKER X CCZMP documentation

**Updated October 29, 2026.** This documentation combines the October 28 working-build audit, the subsequent Autonomous Life V1 implementation and the published CCZMP Locks test harness. It summarizes recorded results; updating the documentation did not include a new full game test run.

| Task | Document |
|---|---|
| Understand the current state | [Project status](STATUS_EN.md) |
| Check all 80 development areas | [Current system register](SYSTEMS_EN.md) |
| Review vehicles and their limitations | [Vehicles](TRANSPORT_EN.md) |
| Understand implementation and tests | [Technical overview](TECHNICAL_EN.md) |
| Choose the next development task | [Roadmap](ROADMAP_EN.md) |
| Find a particular source document | [Complete index](INDEX.md) |
| Compare earlier and current findings | [Changes and sources](CHANGES_EN.md) |
| Explore published source code | [CCZMP Locks](../modules/cczmp-locks/README.md) |

## Reading status labels

“Tested” applies to a specific scenario. The presence of a model, script, configuration or interface does not establish that a mechanic is complete. Mock tests and native engine tests are recorded separately.

The pilot involving three Investigative Committee employees describes an earlier stage. The later [minimal V1 core](snapshot-2026-10-28/13_Autonomous_Life_V1/README.md) covers 22 existing residents; the full simulator specified in the design has not passed acceptance testing. Successful reloads after adding precache protection do not resolve every known crash.

## Sources and history

The [selected October 28 materials](snapshot-2026-10-28/README.md) include original concepts, guides, reports and plans from different dates. The [full audit](snapshot-2026-10-28/CCZMP_PROJECT_FULL_REPORT_2026-10-28.md) preserves the findings of its own stage; later clarifications appear in the current system register. The [old installation index](archive/INDEX-legacy-2026-10-02.md) and [early concepts](../CCZMP/) are also retained.

The complete local document archive, binary models, saves and internal dependency database are not part of this publication. [FILES.json](../../FILES.json) lists the public repository files. See [index maintenance](INDEXING_EN.md) for rebuilding instructions.

## Languages

All 87 source documents have English counterparts, including the historical prose stored as `.txt` and `.ltx`. Each translated page links to its Russian original. See the [translation notes and glossary](../TRANSLATION.md) for terminology, scope and maintenance.
