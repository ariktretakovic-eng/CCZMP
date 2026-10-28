[Русский](../../../../snapshot-2026-10-28/13_Autonomous_Life_V1/KNOWN_LIMITATIONS.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# Boundaries of the current slice

The full V1 for technical specification has not yet been accepted. The minimum vertical from section 14 is implemented here; statuses of native tests - in TEST_REPORT.md.

* Existing residents of the IC base and the Dead City criminal area are registered. The first identity binding requires an already existing UID or the appearance of an NPC online. Other NPCs do not automatically connect. There is no respawn.
* The only food supplier is the current merchant of the area. The stock is finite, there is no production replenishment or inter-location supply. The test profile creates a clear supply of real bread; In a normal game, a test stock is not created.
* There is no second money system. Government contracts may go unpaid with empty coffers; This cannot be considered a successful payment.
* Close physical life uses the previous schemes of three employees IC. For other citizens, new goals have not yet turned into separate trips to the canteen/employer. NPC teleportation or remote physical combat does not occur.
*Career transitions are limited to existing organization and ranks. Political appointment requires an additional legal rule. There is no full training, elections, change of organization and independent management of all departments.
* Relationships and address information are saved; Full integration of the witness silence policy into the investigation has not yet been completed. No criminal proceeds are generated. Groups take into account real members, their accounts, leadership and logical influence; Autonomous robberies, recruitment, deals and wars are not accepted.
* Physical death from offline hunger has not been implemented. Native death blocks further life; the absence of an object is not considered evidence of death.
* Queue is limited by the number of events and budget; The transfer of playing time is catching up gradually. There is no separate aggregated recalculation for the years yet.
* An individual event error is quarantined; the event is not declared successful. Automatic world/save erasing does not apply. Recovery of a corrupted custom schema is not complete.
* The well-known transport warm-load `0xC0000005` dated 10/22 is a separate, unclear defect. A new successful test does not prove it has been fixed.
* Benchmark 100/1000/5000 - logical NPCs under LuaJIT with a mock environment. This is not an FPS game or a confirmation of the work of so many physical NPCs.
