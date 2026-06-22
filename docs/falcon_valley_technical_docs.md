# Falcon Valley — Technical Architecture Documentation

## 1. Overview

Falcon Valley is an asynchronous strategy simulation platform designed to model decision‑making, negotiation, and economic interactions between players. The system integrates a Telegram bot interface, a modular game engine, scenario generation, and persistence through a MongoDB database.

The platform focuses on scenario‑based interactions, market participation, and player‑to‑player strategic decisions. Each interaction produces measurable outcomes such as capital changes, reputation adjustments, trust modifications, and access to new opportunities.

The architecture is designed around modular layers that separate interface logic, business logic, and infrastructure.

Core design goals:

- modular architecture
- asynchronous execution
- scalable game session management
- separation of domain logic from messaging interface
- extensible scenario and market system

---

# 2. System Architecture

The system follows a layered architecture.

```
Telegram Interface
        │
        ▼
Bot Layer
(callbacks, UI, message routing)
        │
        ▼
Service Layer
(application logic / orchestration)
        │
        ▼
Game Engine Layer
(core game mechanics and simulations)
        │
        ▼
Data Layer
(database access and models)
```

Supporting modules:

- AI modules (scenario generation / evaluation)
- utility modules (logging, helpers)

---

# 3. Core Components

## 3.1 Bot Layer

Responsible for communication with Telegram and translating user interactions into internal commands.

Main responsibilities:

- receiving updates
- routing callback queries
- formatting responses
- presenting UI components

Key modules:

```
bot/
    telegram_api.py
    callback_manager.py
    ui.py
```

### Telegram API

Provides a minimal wrapper around the Telegram Bot API.

Responsibilities:

- send_message
- edit_message
- answer_callback
- polling loop

Example interface:

```
class TelegramBotAPI:

    async def send_message(self, chat_id, text, reply_markup=None)

    async def edit_message(self, chat_id, message_id, text)

    async def answer_callback(self, callback_id, text=None)
```

---

### Callback Manager

The callback manager dispatches callback queries to specific handlers.

Callback data format:

```
action:arg1:arg2
```

Examples:

```
deal_accept:deal_id
deal_reject:deal_id
quiz_ans:scenario_id:option
market_global
strategy_war
choice_cooperate
```

Processing pipeline:

```
callback query
   ↓
parse action
   ↓
route to handler
   ↓
execute service logic
   ↓
update UI
```

---

### UI Layer

UI module builds Telegram message layouts.

Responsibilities:

- generating keyboards
- formatting scenario messages
- presenting deal options
- displaying game results

Example:

```
UI.build_scenario_message(scenario)
UI.build_market_keyboard(markets)
UI.build_deal_buttons(deal_id)
```

---

# 4. Service Layer

The service layer orchestrates domain logic and database operations.

Services coordinate between:

- bot layer
- game engine
- database models

Structure:

```
services/
    deal_service.py
    session_service.py
    state_service.py
    judge_service.py
    question_factory.py
```

---

## Deal Service

Handles lifecycle of deals.

Responsibilities:

- validating player eligibility
- checking balance and trust
- resolving deal outcomes
- updating player profile

Main operations:

```
create_deal()
accept_deal()
reject_deal()
resolve_deal()
```

Example flow:

```
User clicks Accept Deal
        ↓
callback_manager
        ↓
DealService.accept_deal()
        ↓
DealEngine.resolve()
        ↓
update UserProfile
        ↓
send result message
```

---

## Session Service

Manages player sessions and game participation.

Responsibilities:

- matchmaking
- active game tracking
- session lifecycle management

Example:

```
create_session(player1, player2)
get_active_session(player_id)
end_session(session_id)
```

---

## State Service

Maintains temporary runtime state.

Examples:

- quiz state
- waiting queues
- strategy selections

This data may remain in memory during runtime.

Example structures:

```
quiz_state = {}
waiting_queue = {}
active_games = {}
```

---

## Judge Service

Evaluates answers in scenario‑based quizzes.

Possible implementations:

- rule based
- LLM assisted
- scoring heuristics

Example interface:

```
judge.evaluate_answer(scenario, answer)
```

Return value:

```
{
    "score": int,
    "feedback": str
}
```

---

## Question Factory

Responsible for generating scenario questions.

Sources:

- database scenarios
- AI generated scenarios
- predefined templates

Example:

```
scenario = question_factory.generate_scenario(market)
```

---

# 5. Game Engine Layer

The game engine contains the deterministic logic of the system.

This layer must remain independent from Telegram or external interfaces.

Structure:

```
game/
    engine.py
    manager.py
    game_loop.py
    scenario_engine.py
    deal_engine.py
    market_factory.py
```

---

## Game Engine

Responsible for calculating outcomes of player decisions.

Example responsibilities:

- payoff calculation
- trust modification
- reputation updates
- outcome resolution

Example:

```
GameEngine.resolve_game(session)
```

Returns:

```
{
    "winner": player_id,
    "player1_reward": int,
    "player2_reward": int
}
```

---

## Game Manager

Controls lifecycle of multiplayer sessions.

Responsibilities:

- creating games
- storing player choices
- resolving rounds
- finalizing sessions

Example flow:

```
match players
    ↓
create GameSession
    ↓
collect strategies
    ↓
resolve game
    ↓
store results
```

---

## Game Loop

Handles scheduled events such as:

- periodic quiz generation
- inactive session cleanup
- matchmaking triggers

Example scheduler:

```
while True:
    await run_quiz_generation()
    await run_matchmaking()
    await asyncio.sleep(1)
```

---

## Scenario Engine

Creates and processes strategic scenarios.

Possible scenario types:

- cooperation vs betrayal
- resource allocation
- negotiation dilemmas
- market investment choices

Example scenario object:

```
Scenario {
    id
    description
    options[]
    correct_option
    market
}
```

---

## Deal Engine

Calculates outcomes of deal interactions.

Input:

```
Deal {
    cost
    risk
    expected_return
    trust_requirement
}
```

Output:

```
DealResult {
    success
    profit
    trust_change
}
```

---

## Market Factory

Loads and manages available markets.

Example markets:

```
local
startup
energy
technology
finance
geopolitics
```

Example interface:

```
market_factory.load_from_db()
market_factory.get_market(name)
```

---

# 6. Data Layer

Responsible for persistence and data models.

Structure:

```
data/
    db_helper.py
    models.py
```

---

## Database

MongoDB is used for persistence.

Driver:

```
Motor (async MongoDB driver)
```

ODM:

```
Beanie
```

Initialization:

```
await init_beanie(database, document_models=[...])
```

---

## Models

Main domain models include:

### UserProfile

```
UserProfile {
    user_id
    username
    capital
    reputation
    trust_score
    score
    games_played
}
```

---

### Scenario

```
Scenario {
    id
    description
    options
    correct_option
    market
    difficulty
}
```

---

### Decision

Represents player decisions during games.

```
Decision {
    player_id
    session_id
    choice
    timestamp
}
```

---

### Deal

```
Deal {
    id
    title
    cost
    expected_profit
    risk
    trust_requirement
}
```

---

# 7. AI Components

AI modules support dynamic content generation and evaluation.

Structure:

```
ai/
    rag_helper.py
```

Possible responsibilities:

- scenario generation
- answer evaluation
- strategic analysis

Example:

```
scenario = rag.generate_scenario(context)
```

---

# 8. Runtime State

Some components maintain runtime memory structures.

Examples:

```
quiz_state
waiting_queue
active_quiz_users
game_sessions
```

These structures manage transient game state that does not require persistent storage.

---

# 9. Execution Flow

Startup process:

```
run.py
   ↓
main()
   ↓
connect_to_database()
   ↓
load markets
   ↓
initialize services
   ↓
start bot polling
   ↓
start scheduler loop
```

---

Example callback flow:

```
User presses button
      ↓
Telegram callback query
      ↓
CallbackManager.parse()
      ↓
CallbackManager.dispatch()
      ↓
Service execution
      ↓
GameEngine calculation
      ↓
Database update
      ↓
UI response sent
```

---

# 10. Concurrency Model

Falcon Valley operates on an asynchronous architecture.

Framework:

```
asyncio
```

Parallel tasks may include:

- Telegram polling
- scheduled game loops
- quiz generation
- matchmaking

Example:

```
asyncio.create_task(quiz_scheduler_loop())
asyncio.create_task(matchmaking_loop())
```

---

# 11. Logging

Centralized logging is handled by the utility logger module.

Responsibilities:

- error tracking
- event tracing
- debugging support

Example:

```
logger.info("Game started")
logger.error("Database connection failed")
```

---

# 12. Scalability Considerations

Potential scaling improvements include:

- distributed game sessions
- Redis for shared state
- message queue for event processing
- horizontal bot instances
- database indexing

Future architecture may include:

```
Bot Workers
Game Engine Workers
Redis State Layer
MongoDB Cluster
```

---

# 13. Security Considerations

Key concerns include:

- validating callback data
- preventing replay attacks
- verifying player ownership of sessions
- rate limiting requests
- secure environment variable storage

Sensitive data should be managed through environment variables.

---

# 14. Future Extensions

Possible extensions include:

- seasonal events
- ranking systems
- tournaments
- advanced negotiation mechanics
- AI opponents
- analytics dashboards
- player reputation networks

---

# 15. Summary

Falcon Valley is designed as a modular asynchronous platform combining:

- a Telegram-based interface
- a deterministic game engine
- scenario-based gameplay
- economic and negotiation mechanics
- AI-assisted decision evaluation

The architecture separates messaging, orchestration, simulation logic, and persistence to ensure maintainability, extensibility, and scalability as the system evolves.
