[Русский](../../../../snapshot-2026-10-28/01_%D0%9E%D0%B1%D1%89%D0%B8%D0%B9_%D0%BA%D0%BE%D0%BD%D1%86%D0%B5%D0%BF%D1%82/STALKER_X_CCZMP_MASTER_CONCEPT-1.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# STALKER X CCZMP - master concept of the project

**Version:** 0.1 · **Status:** concept and long-term vision, NOT a list of implemented features.  
**Base:** S.T.A.L.K.E.R. Anomaly 1.5.1 / X-Ray (hereinafter referred to as engine modifications).  
**Notations:** **[AUTHOR]** - an idea directly voiced by the creator; **[DETAILS]** - logical disclosure of the idea; **[SUGGESTION]** - new option for consideration; **[SOLVE]** is an open architectural issue.

## 0. Mission and principles

- **[AUTHOR]** Create a large-scale RP world in the S.T.A.L.K.E.R. universe, accessible to everyone, combining realism, maximum freedom of action, plot and free play. The player himself chooses what to do, with whom to communicate, where to live and whether to participate in public life at all.
- **[AUTHOR]** Preserve the atmosphere of the original S.T.A.L.K.E.R.: loneliness, abandonment, melancholy, dark forests, cemeteries, familiar places, nostalgia. Along with them are living megacities, villages, industrial areas, steppes and transport hubs.
- **[AUTHOR]** The world should allow you to simply exist: sit at the station, wait for the train, drink tea in a compartment, walk through the forest, watch people. Not every action has to be a quest or earnings.
- **[AUTHOR]** Maximum interconnected mechanics, real consequences of decisions, the possibility of a quiet, official, entrepreneurial or criminal life.
- **[DETAILS]** System simulation instead of a set of unrelated scripts: transport affects logistics, logistics affects trade, trade affects the economy, economy affects work, taxes, crime and everyday life.
- **[AUTHOR]** Long-term project with a horizon of 10–20+ years; Use compatible existing mods and resources while respecting permissions, licenses, and credit. AI is a development assistance tool.

## 1. Game modes

### 1.1 Offline
- **[AUTHOR]** Full-fledged single-player game: optional plot or free sandbox.
- **[AUTHOR]** NPC with an autonomous life, character, goals, memory, relationships and unique reactions.
- **[AUTHOR]** Folder `gamedata` with configs and resources open for reading and editing by the user.
- **[DETAILS]** Local saves and local world state; events outside the active location are calculated in a simplified manner, without continuous expensive physical simulation.

### 1.2 Online
- **[AUTHOR]** One shared persistent RP world and one official game server as a service managed by the creator; no independent worlds with different economies.
- **[AUTHOR]** Architectural guideline: 1000–2000 simultaneously connected players, no promise of capacity achieved.
- **[AUTHOR]** The main roles are performed by real players. Online NPCs are **not confirmed yet**: preliminary idea - players only, but final decision is open.
- **[DETAILS]** A single logical world can be served by several physical processes/machines: regional simulation, unified accounts, economics, property rights, inter-regional events.
- **[DETAILS]** Authoritative server: the server verifies monetary transactions, inventory, property, transport, interactions and access rights; local client files are not the source of truth.
- **[SOLVE]** Seamless map or X-Ray levels with transitions; player scaling and migration scheme; presence/absence of limited service NPCs; Custom Client Modification Policy.

## 2. NPC: full-fledged life simulation (key offline direction)

### 2.1 Personality and uniqueness
- **[AUTHOR]** Each NPC has its own character, goals, habits, attitude towards the player and other NPCs, and life circumstances.
- **[AUTHOR]** NPC can be friendly, neutral, arrogant, aggressive, anxious, bold, indifferent, etc.; character is not reduced to a fixed reaction.
- **[AUTHOR]** Character, beliefs and goals change over time under the influence of events, experiences and relationships.
- **[DETAILS]** Parameters: temperament, impulsiveness, trust, empathy, ambition, moral values, skills, fatigue, stress, needs, social status, finances.
- **[DETAILS]** Separate stable personality traits and short-term states: a brave person can be afraid, an anxious person can decide to take risks.

### 2.2 Reactions to what is happening
- **[AUTHOR]** Different reactions to threats, hostages, conflicts, attacks, requests for help: silence, negotiations, panic, resistance, insults, requests to let go, attempts to help others.
- **[AUTHOR]** NPCs themselves can attack the player, protect him, avoid him, trust him or not trust him.
- **[DETAILS]** Reaction depends on relationships, memories, current state, social role, risk assessment, witnesses, past experience.
- **[DETAILS]** External behavior: poses, facial expressions (if supported by models), gestures, animations, voice, distance, pauses, gaze, use of objects.

### 2.3 Autonomous life and life events
- **[AUTHOR]** Work, earnings, debts, loans, calls, relationships, divorce, finding accommodation, friendship, conflicts, moving, changing profession, changing life goals.
- **[AUTHOR]** Example: wife reports divorce; creditors demand payments; The NPC goes out to smoke and ponders the situation; after work he asks a friend to spend the night; a friend’s consent or refusal changes the future of life.
- **[AUTHOR]** Favorable, neutral and tragic outcomes are possible; crimes, cruelty, psychological crises and death as part of a serious world without necessarily idealizing the characters.
- **[DETAILS]** Psychological crises should not be reduced to the formula “bullying = crime” or “stress = suicide”: take into account the diversity of outcomes, social support and assistance; avoid sensationalism.
- **[DETAILS]** NPC can read, sleep, make calls, use the computer, relax, go on vacation, make purchases, and do household chores without the player’s participation.

### 2.4 Social relationships and memory
- **[AUTHOR]** NPC remembers the player and other NPCs, their help, deception, threats, joint events; relationships change.
- **[AUTHOR]** NPCs can have friends, spouses, children, families, colleagues, enemies, business partners.
- **[AUTHOR]** Over the years, an NPC can change jobs, open a business, move, take a government position; the player will discover changes when meeting again.
- **[DETAILS]** Social connections graph, biographical memory, events and consequences; long-term memory stores what is essential, not all cues in a row.

### 2.5 Equality between NPC and player
- **[AUTHOR]** An NPC can become a minister, a civil servant, a security official, an entrepreneur, a hacker, a corrupt official, a criminal, a utility employee, or an ordinary resident.
- **[AUTHOR]** NPCs can buy property, open businesses, hire other NPCs or the player (if the regime allows), participate in the economy and social processes.
- **[DETAILS]** General rules of ownership, employment, economics, reputation and rights; What may vary is the computational detail, not the legal capabilities.

### 2.6 AI scaling
- **[DETAILS]** Near the player - full physics, navigation, interactions; at a distance - simplified actions; far away - rare events and status updates.
- **[OFFER]** Utility AI + GOAP scheduling + memory + social graph; Language models are optional for dialogues, not for every step of the simulation.
- **[SOLVE]** Simulation frequency, active NPC limits, time flow, offline progress and persistence rules.

## 3. Transport: full spectrum

### 3.1 Ground personal
- **[AUTHOR]** Passenger cars, SUVs, sports, exclusive, luxury cars; off-road vehicles.
- **[DETAILS]** Sedans, station wagons, hatchbacks, coupes, pickups, minibuses, motorcycles, trucks, tractors, special equipment, ATVs.
- **[DETAILS]** Wear and tear of engine, suspension, tires, brakes, body; fuel, repair, maintenance, diagnostics, garage work, spare parts.

### 3.2 Public and official
- **[AUTHOR]** Buses, public transport, state, official, departmental and special transport.
- **[DETAILS]** Minibuses, trolleybuses, trams, taxis, school buses, ambulances, fire trucks, police, OMON, utility vehicles, tow trucks, garbage trucks, postal transport.
- **[DETAILS]** Routes, stops, schedules, tickets, driver changes, transportation of passengers and cargo.

### 3.3 Railway and underground
- **[AUTHOR]** Full-fledged trains, railway lines and stations; free movement through carriages, compartments, corridors, toilets, the opportunity to sit down, lie down, communicate, drink tea and watch the scenery.
- **[AUTHOR]** Underground transport.
- **[DETAILS]** Passenger, freight, commuter trains; metro, underground service trains; locomotives, depots, switches, signaling, platforms, conductors, schedules.
- **[DETAILS]** Travel between cities, stops in villages, night flights, luggage, tickets, delays, travel companions.
- **[SOLVE]** New routes and paths via SDK; physics of characters on moving platforms; synchronization of cars and transitions between levels.

### 3.4 Air and water
- **[AUTHOR]** Full-fledged flying and water transport.
- **[DETAILS]** Helicopters, airplanes, small aircraft, specialized aviation; boats, boats, ferries, barges, river vessels.
- **[DETAILS]** Boarding/disembarking, management, transportation, parking, repairs, weather conditions, traffic safety.

### 3.5 Road infrastructure
- **[AUTHOR]** Real wear and tear on roads.
- **[DETAILS]** Potholes, coverings, repair crews, road works, accidents, speed limits, traffic lights, signs, traffic police, evacuation, fines.

## 4. Real estate and property

- **[AUTHOR]** Dormitories, apartments, apartment buildings, private houses, cottages, villas, garages, warehouses, pickup points, bars, restaurants, company offices, skyscrapers.
- **[AUTHOR]** Each building must belong to someone: a player, an NPC, an organization, a company or a state (according to the rules of the world).
- **[DETAILS]** Hangars, workshops, car service centers, parking lots, underground parking lots, hotels, hostels, shops, shopping pavilions, land plots, dachas, farms, industrial facilities.
- **[DETAILS]** Purchase, sale, rent, sublease, access by keys/roles, utility bills, repairs, redevelopment, furnishing, storage of things, security, inheritance, seizure by law.
- **[OFFER]** Cadastre, register of owners, property taxes, contracts, mortgages, insurance, auctions, bankruptcy.

## 5. Public, commercial and official places

- **[AUTHOR]** Shopping centers and shopping centers, bus stations, bus stations, railway depots, stations and terminals, bus depots, agencies, company offices.
- **[DETAILS]** Airports, airfields, ports, marinas, stops, ticket offices, control rooms, logistics centers, warehouses and sorting points.
- **[DETAILS]** Shops, markets, supermarkets, cafes, canteens, restaurants, bars, hotels, cinemas, gyms, stadiums, clubs, museums, libraries, post office, banks, ATMs.
- **[DETAILS]** Hospitals, clinics, pharmacies, schools, kindergartens, universities, colleges, schools, hostels, service centers, service stations, tire shops, car washes.
- **[DETAILS]** Industrial buildings: plants, factories, oil rigs, quarries, mines, power plants, farms, greenhouses, elevators.
- **[OFFER]** Possibility of real functioning of institutions: employees, opening hours, goods, services, purchases, salaries, supplies.

## 6. State, law and security forces

- **[AUTHOR]** State Department / Council of Ministers, Ministry of Internal Affairs, OMON, “Alpha”, Investigative Committee, prosecutor’s office, court, FSIN, UES, other bodies and departments.
- **[AUTHOR]** Regular, medium and high security prisons; protected areas; regular and secret laboratories.
- **[DETAILS]** Administrations of cities and regions, ministries, tax authorities, customs, border services, fire departments, rescue stations, communication centers, archives, state registers.
- **[DETAILS]** Police stations, investigation departments, crime laboratories, pre-trial detention centers, temporary detention centers, correctional facilities, courts, prosecutor's offices.
- **[AUTHOR]** Arrests, fines, criminal and administrative liability, corruption and anti-corruption.
- **[DETAILS]** Statements, investigations, evidence, witnesses, warrants, searches, lawyers, court hearings, verdicts, appeals, prison terms, release.
- **[SOLVE]** Jurisdictions and fictional law of the world; roles and limitations of authority; protection from abuse by administration and players.

## 7. Crime and the shadow world

- **[AUTHOR]** Criminal organizations, showdowns, corrupt officials, criminal connections in prisons, organizing escapes for money, fake documents.
- **[AUTHOR]** Difficult events and violence can exist in the world as part of a realistic RP, without a forced positive outcome.
- **[DETAILS]** Smuggling, underground markets, theft, fraud, extortion, organized groups, illegal transactions, struggle for territory, investigation and trial.
- **[DETAILS]** Forgeries as in-game objects with authentication, risks and legal consequences, rather than instructions for actually forging documents.
- **[SUGGESTION]** Reputation, informants, conflicts of interest, prison hierarchy, rehabilitation, crime prevention, in-game complaint mechanisms.

## 8. Economics, banks and finance

- **[AUTHOR]** Banks, loans, deposits, microloans, monetary relations, ownership of real estate and enterprises.
- **[DETAILS]** Accounts, transfers, salaries, cash, payments, rent, taxes, duties, utility bills, debts, arrears, credit history, pledges, bankruptcy.
- **[DETAILS]** Production and consumption of goods, supplies, warehouse balances, prices, logistics, stores, government procurement, organization budgets.
- **[SUGGESTION]** Inflation, money issues, economic crises, insurance, investments, exchanges, operating licenses, anti-monopoly mechanisms.
- **[SOLVE]** Sources and drains of game currency, income balance, anti-dupe, protection of the economy from monopolies and exploits, donation admissibility.

## 9. Professions and work

- **[AUTHOR]** More than 100 professions as a long-term goal: from photographer, street cleaner and courier to cybersecurity specialist, engineer and civil servant.
- **[AUTHOR]** Large labor areas: utilities, industry, oil rigs, quarries, factories, government agencies, law enforcement agencies, IT and hacker communities.
- **[DETAILS]** Professions: driver, driver, conductor, dispatcher, pilot, sailor, auto mechanic, welder, electrician, electronics engineer, builder, road worker, plumber, power engineer, miner, oil worker, factory worker, farmer, doctor, paramedic, teacher, journalist, lawyer, accountant, programmer, system administrator, analyst, salesman, cook, security guard, rescuer, investigator, judge.
- **[DETAILS]** Each job has activities, tools, skills, qualifications, schedules, employers, pay, career opportunities and consequences of mistakes.
- **[OFFER]** Employment contracts, vacancies, interviews, internships, advanced training, trade unions, strikes, labor protection.

## 10. Education and engineering

- **[AUTHOR]** Education at universities, colleges, schools and independently using textbooks; many specialties.
- **[AUTHOR]** Engineering: soldering, welding, electronics, electrical and other technical areas.
- **[DETAILS]** Curricula, classes, practice, exams, diplomas, licenses, internships, workshops, laboratory work.
- **[DETAILS]** Repair and creation of objects, electrical networks, circuits, diagnostics, equipment maintenance, tools, consumables and quality of work.
- **[OFFER]** Textbooks with game knowledge, practical work simulators, training from mentors, confirmation of qualifications.

## 11. Daily life, communication and atmosphere

- **[AUTHOR]** Complete trips: station, ticket, waiting for the train, boarding, compartment, luggage, tea with fellow travelers, conversations, spending the night in the carriage, walking along the corridor, getting off at the desired station.
- **[AUTHOR]** NPCs or players can talk, ignore, make friends, conflict; there is a place in the world for the lone traveler.
- **[AUTHOR]** Gloomy cemeteries, dark forests, desert locations, original atmosphere of S.T.A.L.K.E.R. and places for nostalgia.
- **[DETAILS]** Change of day and night, weather, environmental sounds, institutional schedules, seasonal activities, leisure, radio, books, phones, laptops, tea, food, sleep, everyday interactions.
- **[OFFER]** Social events: weddings, holidays, funerals, homecomings, exhibitions, concerts, competitions, social gatherings.

## 12. Geography and locations

- **[AUTHOR]** Megacities, small towns, villages, forests, steppes, industrial zones, abandoned areas, roads and railways.
- **[AUTHOR]** Preservation of familiar locations and atmosphere of the original S.T.A.L.K.E.R.; creation of many new routes and stations via SDK.
- **[DETAILS]** Residential areas, historical centers, suburbs, suburban areas, highways, tunnels, bridges, quarries, mines, fields, reservoirs, ports, airfields, closed areas.
- **[SOLVE]** Seamlessness, regional boundaries, world streaming, loading, transport between locations, distances and time scale.

## 13. Character, life and death

- **[AUTHOR]** One life mechanic: after the death of a character, the player starts over with another character.
- **[DETAILS]** Biography, documents, social status, skills, health, reputation, education, property, connections and history of the character.
- **[DECIDE]** The fate of property and organizations after death, inheritance, technical protection from death due to a bug, disconnection, disputes and abuse.

## 14. Plot and freedom

- **[AUTHOR]** The plot exists, but is not required; the player can ignore it completely and move on with their lives.
- **[DETAILS]** Several directions of history, tasks and consequences of choices, histories of organizations and regions, independent events without reference to the main character.
- **[OFFER]** Local story arcs, investigations, profession chains, stories of individual NPCs and families.

## 15. Technical foundation

- **[AUTHOR]** Based on Anomaly 1.5.1 and X-Ray; deep modification of the engine, use of SDK and existing mods as needed.
- **[DETAILS]** Key subsystems: saves, events, inventory, interactions, transport physics, network code, synchronization, authorization, server economy, rights system, logging, anti-cheat.
- **[DETAILS]** For moving vehicles - local coordinate systems, boarding/disembarking, moving around the cabin, collisions, passenger synchronization.
- **[DETAILED]** For MMO - interest management (transferring only relevant objects to the client), spatial division of the simulation, load tests, failure recovery, backups, monitoring.
- **[DETAIL]** For NPCs - separate simulation layer, personality/memory/connection data, deterministic or verifiable events, AI detail levels.
- **[OFFER]** Modular architecture, unified registry of entities, event system, automated tests, CI, API and data schema documentation.

## 16. Target online and social density

- **[AUTHOR]** Ideally 1000-2000 concurrent players to fill organizations, professions and cities.
- **[AUTHOR]** Examples of the desired scale: about 50 OMON employees, 200–260 utility workers, 100–150 members of a hacker group, 200–250 people in government and law enforcement agencies, hundreds of civil and industrial workers.
- **[DETAILS]** Do not rely on the ideal distribution of professions: with low online, some systems should work in a limited mode or automatically.
- **[SUGGESTION]** Gradually open up districts and organizations as the community grows, maintaining one logical world.

## 17. Implementation priorities (proposal, unapproved plan)

1. **Foundation:** stable offline, events, saves, inventory, basic interactions, error log.
2. **Vertical slice:** one settlement, several professions, property, transport, economy and consequences of actions.
3. **Transport prototype:** one vehicle with service; then one carriage and a short route with free movement.
4. **NPC Living World:** needs → schedules → memory → relationships → economy → autonomous goals and events.
5. **Online prototype:** connection, authoritative server, synchronization, secure economy, load testing.
6. **Social infrastructure:** work, enterprises, state, law, crime, education.
7. **Scaling:** new areas, transport networks, professions, complex chains of economics and social events.

## 18. Register of open solutions

- [ ] Seamless map or transitions between levels?
- [ ] Will there be limited service NPCs online or only players?
- [ ] How much game time corresponds to a real hour?
- [ ] How to simulate absent NPCs and how long does it take without a player?
- [ ] How to handle death from a bug with permanent death?
- [ ] How is property preserved after the death of a character?
- [ ] What is the model of a single world on several physical servers?
- [ ] How to prevent inflation, dupes, abuse of power?
- [ ] What existing mods are allowed to be integrated and under what conditions?
- [ ] What is the minimum version of the game to release first?
- [ ] What elements are available for free and how to ensure a fair economy?
- [ ] What rules and age restrictions are needed for heavy plots and violence?

## 19. Template for adding a new idea

**ID:** CCZMP-IDEA-0001  
**Name:**  
**Category:** NPC / transport / economics / law / map / professions / other  
**Source:** [AUTHOR] / [SUGGESTION]  
**Gist:**  
**As the player sees it:**  
**Which systems are affected:**  
**Dependencies:**  
**Technical risks:**  
**Priority:** idea / prototype / later  
**Status:** not started / research / prototype / implemented / tested  

---

**Note:** This document records the ideas discussed and their development. It does not represent that the features listed have already been implemented, and is not a substitute for a detailed statement of work, architectural specification, or task register.
