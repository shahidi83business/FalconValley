#gameloop.py
from transitions.extensions.asyncio import AsyncMachine

from models import RoundSession, StatusEnum
from engine import GameEngine
from state_service import StateService


class GameLoop:
    def __init__(self, session: RoundSession, players_info: list):
        self.session = session
        self.game_id = str(session.id)
        self.players = players_info

        self.choices = {}
        self.strategy = {}
        self.war_choices = {}
        self.war_penalty = {p["id"]: 0 for p in players_info}
        self.market_id = session.market_id

        initial_budget = 1000
        self.budgets = {p["id"]: initial_budget for p in players_info}
        self.investments = {}

        states = [
            "idle",
            "waiting_strategy",
            "waiting_negotiation",
            "decision",
            "war_decision",
            "completed",
        ]

        self.machine = AsyncMachine(
            model=self,
            states=states,
            initial=session.fsm_state or "idle",
            after_state_change="sync_db",
        )

        self.machine.add_transition("start_game", "idle", "waiting_strategy")
        self.machine.add_transition(
            "start_negotiation",
            "waiting_strategy",
            "waiting_negotiation",
        )
        self.machine.add_transition(
            "start_decision",
            "waiting_negotiation",
            "decision",
        )
        self.machine.add_transition(
            "start_chicken",
            "waiting_strategy",
            "war_decision",
        )
        self.machine.add_transition("finish", "*", "completed")

    async def sync_db(self):
        self.session.fsm_state = self.state

        if self.state == "completed":
            self.session.status = StatusEnum.completed

        existing_game_data = self.session.game_data or {}

        existing_game_data.update({
            "choices": self._stringify_keys(self.choices),
            "strategy": self._stringify_keys(self.strategy),
            "war_choices": self._stringify_keys(self.war_choices),
            "war_penalty": self._stringify_keys(self.war_penalty),
            "budgets": self._stringify_keys(self.budgets),
            "investments": self._stringify_keys(self.investments),
        })


        self.session.game_data = existing_game_data

        await self.session.save()

    def is_everyone_ready(self, dict_name):
        target_dict = getattr(self, dict_name)
        return len(target_dict) == len(self.players)

    def _get_player_ids(self):
        return [p["id"] for p in self.players]

    def _get_game_mode(self):
        """
        Determines which game path should be finalized.

        Current logic:
        - if war_choices exists for all players => CHICKEN / WAR
        - elif choices exists for all players => NEGOTIATION
        - else fallback based on strategy
        """

        if self.is_everyone_ready("war_choices"):
            return "CHICKEN"

        if self.is_everyone_ready("choices"):
            return "NEGOTIATION"

        if self.is_everyone_ready("strategy"):
            return "STRATEGY"

        return "UNKNOWN"

    async def _stringify_keys(self, value):
        if isinstance(value, dict):
            return {
                str(key): self._stringify_keys(inner_value)
                for key, inner_value in value.items()
            }

        if isinstance(value, list):
            return [self._stringify_keys(item) for item in value]

        return value

    async def finalize(self):
        """
        Final step of the game loop:
        1. Detect mode
        2. Calculate outcome with GameEngine
        3. Apply effects with StateService
        4. Save outcome in session.game_data
        5. Finish session
        """

        mode = self._get_game_mode()

        if mode == "NEGOTIATION":
            outcome = await GameEngine.calculate_negotiation_outcome(
                session=self.session,
                players=self.players,
                choices=self.choices,
            )

        elif mode == "CHICKEN":
            outcome = await GameEngine.calculate_chicken_outcome(
                session=self.session,
                players=self.players,
                war_choices=self.war_choices,
                war_penalty=self.war_penalty,
            )

        elif mode == "STRATEGY":
            outcome = await GameEngine.calculate_strategy_outcome(
                session=self.session,
                players=self.players,
                strategy=self.strategy,
            )

        else:
            outcome = {
                "mode": "UNKNOWN",
                "scores": {},
                "effects": {"economy": {}},
                "result_text": "Game finalized without enough decisions.",
                "error": "not_enough_player_inputs",
            }

        apply_result = await StateService.apply_pvp_outcome(
            session=self.session,
            players=self.players,
            outcome=outcome,
        )

        if not self.session.game_data:
            self.session.game_data = {}

        self.session.game_data["outcome"] = self._stringify_keys(outcome)
        self.session.game_data["state_apply_result"] = self._stringify_keys(apply_result)

        await self.session.save()
        await self.finish()
