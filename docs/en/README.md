[Русский](../../README.md) · **English** · [Documentation index](docs/INDEX.md) · [Translation notes](TRANSLATION.md)

# STALKER X CCZMP

**A roleplay project built on S.T.A.L.K.E.R. Anomaly 1.5.1 / X-Ray (Monolith)**

The project is developing a detailed offline world with organizations, legal and economic systems, documents, vehicles and persistent NPC lives. Research into network architecture is planned as a separate stage after the offline build is stable. **Working multiplayer is not currently claimed.**

> **The project is in development.** This repository provides public documentation and an entry point for contributors. It is not a complete game archive or a finished release.

## Current state (updated October 29, 2026)

CCZMP is a substantial **offline prototype**, not a finished game. Analysis of the working build and recorded tests shows:

- **41 organizations** in the in-game registry; not every organization has a complete operational workflow.
- **The F6/F7 terminal**, identity documents, investigations, prosecution, courts, warrants and custody escorts have recorded in-game tests, but not every scenario is complete.
- **197 entries** in the main item catalog and **51 application entries**. These counts do not mean that all entries represent complete, independent mechanics.
- **85 vehicle configuration sections with OGF resources**, including service vehicles and drones. A model and configuration section do not establish that each vehicle has passed driving tests.
- **Autonomous Life V1**: a minimal core for 22 existing Dead City residents, with persistent state, needs, work and finances. The complete specification has not passed acceptance testing; loading and behavior limitations remain.
- Work in progress includes aviation, passenger systems and trains, industrial economics, property, fully developed professions, voice acting, broader autonomous NPC AI and stabilization.

**[Documentation](docs/README.md)** · **[Project index](INDEX.md)** · **[Current status](docs/STATUS_EN.md)** · **[80 development areas](docs/SYSTEMS_EN.md)** · **[Vehicles](docs/TRANSPORT_EN.md)** · **[October 28 source materials](docs/snapshot-2026-10-28/README.md)** · **[Technical overview](docs/TECHNICAL_EN.md)** · **[Roadmap](docs/ROADMAP_EN.md)** · **[Contributing](CONTRIBUTING.md)**

## Published source code and tests

**[CCZMP Locks — source-code showcase](modules/cczmp-locks/README.md)** includes portable PIN cases, preservation of original items through ALife, deferred item transfers and in-world lock opening. Its source code and a minimal test environment are published. All 21 focused tests passed in a repeat run on October 29, 2026. This is a **source showcase**, not a standalone installable mod or evidence that the entire current game build has been tested.

## Volunteer contributors wanted

Current needs include Lua / Anomaly 1.5.1, X-Ray UI and persistence, NPC AI, Blender/X-Ray OGF/OMF, vehicle physics, HUD animations and testing. Participation is **voluntary, with no guaranteed payment or mandatory schedule**. You do not need the full gamedata to get started. Share a portfolio and discuss a small, clearly scoped task.

## Rights and publication

Game source code and third-party assets are not automatically included in public releases. Models, animations and code remain subject to their respective licenses or permissions from rights holders. This documentation does not grant access to the private game archive.

## Historical name

The original designation was STALKER x CCZMP v0.1 BETA. Current feature statuses are documented separately and do not imply a finished public release.
