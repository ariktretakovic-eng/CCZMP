[Русский](../../STATUS_RU.md) · **English** · [Documentation index](INDEX.md) · [Translation notes](../TRANSLATION.md)

# STALKER X CCZMP — public development status

**Updated October 29, 2026. Based on the October 28 local-build audit and the Autonomous Life V1 implementation report.**

CCZMP is built on S.T.A.L.K.E.R. Anomaly 1.5.1 / X-Ray. This is a snapshot of features at different stages of completion. “Tested” refers to the recorded scenarios, not every possible combination of conditions.

| Subsystem | Current state | Limitations / next steps |
|---|---|---|
| F6/F7, windows and controls | Tested in selected scenarios | Regression after integration, different resolutions and loading |
| Organization registry | 41 organizations registered in-game; partial integration | Not all organizations have a complete workflow, base and equipment |
| Documents, criminal and administrative law | Items, cases, warrants and the IC → prosecution → court chain are implemented; some scenarios tested in-game | No complete procedural simulation or document-presentation animations |
| Investigations, evidence and custody escorts | Limited scenarios cover IC deployment, inspection, item transfers and NPC delivery | Not all witness, disguise, route and save scenarios have been tested |
| Gadgets and the in-game network | Physical UIDs, operating systems, SIM cards, messages, stores, in-game services and tools | 51 application entries do not imply 51 complete independent apps; these are not real operating systems or real internet access |
| Items, workshop and medicine | 197 main catalog entries; tools, recipes, medicine and containers; some tested | Dedicated models and complete production chains remain |
| Cars and heavy equipment | Basic car and tank scenarios have been tested; the catalog contains 85 vehicle sections with OGF resources | Individual driving tests for new models remain incomplete; all 85 are not fully accepted vehicles |
| Taxis, towing and 111 services | Local tests of journeys, towing, requests and crews | No complete inter-location taxi system, common passenger controller or full service-scenario coverage |
| Aviation, trains, metro and cranes | Prototype resources/configuration sections and individual mechanics | Dedicated flight/rail physics, crane functions and passenger systems are incomplete |
| Voice of Pripyat radio | Broadcasts, music inserts and world/PDA/car radios have individual tests | Voice acting, recording rights and full regression remain |
| Local city and NPCs | Deliveries, local infrastructure, criminal district, reputation and service NPCs | Not all locations or professions are covered |
| Autonomous Life V1 | A minimal event-driven core for 22 Dead City residents; economic transactions and cold loading have tests | The full V1 is not accepted; a warm-load crash was recorded; families, full GOAP and the complete social simulator are unfinished |
| Banking | Personal accounts, transfers, loans and deposits, with partial testing | Corporate accounting, taxes, budgets and a complete ledger remain |
| Industry, real estate and factories | Technical concepts and isolated mechanics | End-to-end production, extraction, supply chains and property are not implemented at the full specification's scale |
| Multiplayer | Planned | No publicly available working shared server for 1,000–2,000 players |

## Documentation and evidence

[Documentation](README.md) · [Complete index](INDEX.md) · [Changes](CHANGES_EN.md)

- [Full project audit, October 28](snapshot-2026-10-28/CCZMP_PROJECT_FULL_REPORT_2026-10-28.md) distinguishes facts, prototypes and plans.
- [Current register of 80 development areas](SYSTEMS_EN.md) combines the audit with subsequent V1 and public-documentation clarifications.
- [85 vehicle configuration sections](snapshot-2026-10-28/12_Project_Audit_2026-10-28/CCZMP_TRANSPORT_CURRENT_2026-10-28.md) records resources and classes, not 85 completed vehicles.
- [Autonomous Life V1 report](snapshot-2026-10-28/13_Autonomous_Life_V1/REPORT_EN.md) and [known limitations](snapshot-2026-10-28/13_Autonomous_Life_V1/KNOWN_LIMITATIONS.md) cover a later, narrower stage. The earlier three-employee IC pilot does not describe that stage's full scope.
- [CCZMP Locks source code and 21/21 mock tests](../modules/cczmp-locks/README.md) provides a published harness rerun on October 29. That run did not test the entire game build.
- [All selected source documents](snapshot-2026-10-28/README.md) includes concepts, engineering guides, tests and reports.

The latest source review examined the local build and recorded logs. It was not a new full in-game acceptance test. Models, interfaces, scripts and test prototypes alone do not establish release readiness. User saves, additional private source files, binary models and third-party working-directory assets are not added to this repository.
