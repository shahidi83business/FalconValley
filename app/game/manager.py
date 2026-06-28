# manager.py
from typing import Dict, Optional
from app.data.models import RoundSession, StatusEnum
from app.game.gameloop import GameLoop
import logging

class GameManager:
    def __init__(self):
        self.games: Dict[str, GameLoop] = {}
        self.player_game: Dict[int, str] = {}

    async def create_game(self, p1_info: dict, p2_info: dict, market_id: str) -> GameLoop:

        session = RoundSession(
            market_id=market_id,
            status=StatusEnum.in_progress,
            fsm_state="idle",
            game_data={}
        )
        await session.insert()
        
        game_id = str(session.id)
        players = [p1_info, p2_info]

        game_instance = GameLoop(session, players)
        
        await game_instance.start_game()

        self.games[game_id] = game_instance
        for p in players:
            self.player_game[p["id"]] = game_id

        logging.info(f"Game {game_id} created and registered in RAM.")
        return game_instance

    def get_game(self, user_id: int) -> Optional[GameLoop]:
        game_id = self.player_game.get(user_id)
        if game_id:
            return self.games.get(game_id)
        return None

    async def end_game(self, game_id: str):
        game = self.games.get(game_id)
        if not game:
            return

        await game.finish()

        for p in game.players:
            self.player_game.pop(p["id"], None)

        self.games.pop(game_id, None)
        logging.info(f"Game {game_id} has been terminated and cleaned up.")

# ایجاد یک نمونه واحد برای استفاده در کل پروژه
game_manager = GameManager()
