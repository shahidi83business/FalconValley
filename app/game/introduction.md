## deal_engine.py

This file is a small but important part of the project that calculates the result of a deal (Deal).

---

**Main responsibility of this file**

This file decides whether a deal is successful or fails, and what impact it has on the player.

In simple terms, whenever a player accepts a deal, this file is executed and determines:

* Whether the deal was successful or not
* How much the player’s money increases or decreases
* How much Trust changes
* What message is shown to the player

---

## deal_service.py

This file (DealService) is responsible for managing the lifecycle of deals.

If the previous file (DealEngine) determines the outcome of a deal, this file handles creating and updating the state of the deal.

---

**Main responsibility of this file**

This file performs three main tasks:

---

**1. Creating a new deal**

* When a player wants to propose a deal to another player, this file creates a new deal and stores it in the database.

---

**2. Accepting a deal**

* If the other player accepts the deal, the deal status is changed from “pending” to “accepted”.

---

**3. Rejecting a deal**

* If the player does not accept the deal, the status is changed to “rejected”.

---

## engine.py

This code is essentially a game decision simulation engine between two players.

In simple terms:
It takes the decisions of two players (such as cooperation, betrayal, war, retreat) and then:

* Assigns each player a score
* Applies effects on character attributes and the overall economy system

---

**1. Negotiation**

Like the game “cooperate or betray”

---

**2. War (Chicken / War)**

Like the game “who backs down first?”

---

**3. Hybrid mode (War vs Negotiation)**

When one player chooses war and the other chooses negotiation

---

## gameloop.py

This file is the main controller of the game flow.

It does not calculate scores; instead, it:

* Advances the game step by step
* Collects player decisions
* Moves to the next stage when both players are ready
* At the end, gets results from the GameEngine
* Stores the result in the database

---

## manager.py

This file is the high-level manager of all games (Game Registry / Game Controller).

If GameLoop is the director of a single game, this is:

“the system that manages all active games in memory and connects players to games”

---

**Main responsibilities**

1. Creating a new game
2. Finding a user’s game
3. Removing a game after it ends

---

## marketfactor.py

This file (marketfactory.py) is the system for creating and managing game markets.

In simple terms:

This is where the “worlds / economic scenarios” of the game are defined, stored, and even generated using AI.

---

**Main responsibilities**

1. Maintaining predefined markets (like Energy and Tech)
2. Loading markets from the database
3. Creating new markets using AI

---

## scenario_engine.py

This file (SimpleScenarioEngine) is a simple system for generating game scenarios and creating opponents (AI + random).

In very simple terms:

This code builds the “story of the game”, generates “rival players”, and prepares a full game round.

---

**Main responsibilities**

1. Creating scenarios using AI (stage story)
2. Generating artificial opponents
3. Putting everything together to prepare a full game round
