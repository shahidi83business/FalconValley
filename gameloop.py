from transitions.extensions.asyncio import AsyncMachine
from models import RoundSession, StatusEnum
from engine import GameEngine


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
            'idle',
            'waiting_strategy',
            'waiting_negotiation',
            'decision',
            'war_decision',
            'completed'
        ]

        self.machine = AsyncMachine(
            model=self,
            states=states,
            initial=session.fsm_state or 'idle',
            after_state_change='sync_db'
        )

        self.machine.add_transition('start_game', 'idle', 'waiting_strategy')
        self.machine.add_transition('start_negotiation', 'waiting_strategy', 'waiting_negotiation')
        self.machine.add_transition('start_decision', 'waiting_negotiation', 'decision')
        self.machine.add_transition('start_chicken', 'waiting_strategy', 'war_decision')
        self.machine.add_transition('finish', '*', 'completed')

    async def sync_db(self):
        self.session.fsm_state = self.state

        if self.state == 'completed':
            self.session.status = StatusEnum.completed

        self.session.game_data = {
            "choices": self.choices,
            "strategy": self.strategy,
            "war_choices": self.war_choices,
            "war_penalty": self.war_penalty
        }
        await self.session.save()

    def is_everyone_ready(self, dict_name):
        target_dict = getattr(self, dict_name)
        return len(target_dict) == len(self.players)

    async def finalize(self):
        await self.finish()
