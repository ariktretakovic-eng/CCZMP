[Русский](../../../../snapshot-2026-10-28/13_Autonomous_Life_V1/README.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Autonomous Life V1 - navigation

Implemented a minimum event core for **22 existing residents Dead City**. Full V1 according to technical specification is not accepted. Resident composition and results refer to implementation reports 10/28, published 10/29; This does not automatically connect all NPCs in the game.

| Question | Document |
|---|---|
| What's implemented | [REPORT_RU](REPORT_EN.md) |
| What's left | [KNOWN_LIMITATIONS](KNOWN_LIMITATIONS.md) |
| What is tested in the engine and mock | [TEST_REPORT](TEST_REPORT.md) |
| What we know about downloads and AV | [WARM_LOAD](WARM_LOAD.md) |
| Performance and measurement limits | [PERFORMANCE](PERFORMANCE.md) |
| API, wealth owners, real money | [API_CONTRACTS](API_CONTRACTS.md) |
| Config and queue limits | [CONFIG](CONFIG.md) |
| Modified files and hashes | [FILES](FILES.md) |
| Shutdown and rollback | [ROLLBACK](ROLLBACK.md) |
| Integration map before changes | [integration_map](integration_map.md) |
| Full target specification | [technical specification V1](../CCZMP_AUTONOMOUS_LIFE_V1_TECH_SPEC_EN_2026-10-28.md) |

Tested limited chains of real work/food/money, saving, returning the same NPCs, address knowledge, group successor, calling 111 and ordering/cancelling a taxi. Families, full GOAP, autonomous criminal economy, supply and behavior of each citizen nearby are not completed. Tests of 100/1000/5000 logical NPCs do not measure the FPS of games with such a population.

[Current system registry](../../SYSTEMS_EN.md) · [All documents](../../INDEX.md)
