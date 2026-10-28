[Русский](../../TRANSPORT_RU.md) · **English** · [Documentation index](INDEX.md) · [Translation notes](../TRANSLATION.md)

# CCZMP transport - current navigation

Updated 10/29/2026 for transport audit 10/28. No new driving tests were carried out when updating the documentation.

**[Full list of 85 sections](snapshot-2026-10-28/12_Project_Audit_2026-10-28/CCZMP_TRANSPORT_CURRENT_2026-10-28.md)** - the main source of models in the working gamedata. The donor folder describes the sources, not the installed state of the game.

| Category in slice | Sections | What does the number mean |
|---|---:|---|
| Active Directory | 76 | Transport sections with resources; including prototypes |
| Taxi | 1 | Separate physical section |
| Drones | 4 | Physical sections; not four fully completed complexes |
| Services 111 | 4 | Separate service sections |
| Total | 85 | Sections with OGF, not 85 unique vehicles verified |

The 11 disabled sections are not included in these 85. The number of OGFs in the entire meshes folder includes base resources and variants and is not equal to the number of machines.

## Partially implemented and tested

There are car and tank scenarios, a separate taxi ride of about 80 m, towing, service requests and crews. The new 10/22 pack contains 25 OGFs: 23 transport sections and two world objects. The presence of all files and section recognition does not replace individual driving checks.

In the stage [Autonomous Life V1](snapshot-2026-10-28/13_Autonomous_Life_V1/TEST_REPORT.md) calling an ambulance with a real car and crew, ordering and canceling a taxi were tested. The full ride and treatment were not tested in this run.

## What else is to come

New cars require driving tests, physics, collisions and save checks. Aviation and rail transport remain prototypes; full flight/rail physics and general passenger controller are not accepted. Some large models are marked `no_place`.

The known transport warm-load `0xC0000005` from 10/22 is not considered corrected by the successful recovery of two machines with cold loading or later NPC tests. [Parsing loads V1](snapshot-2026-10-28/13_Autonomous_Life_V1/WARM_LOAD.md) preserves individual results and cause uncertainty.

Sources: [systems registry](SYSTEMS_EN.md), [donor package and integration queue](snapshot-2026-10-28/README.md), [original full audit](snapshot-2026-10-28/CCZMP_PROJECT_FULL_REPORT_2026-10-28.md).
