# manager.py
from typing import Dict, Optional
from models import RoundSession, StatusEnum
from gameloop import GameLoop
import logging

class GameManager:
    def __init__(self):
        # ذخیره نمونه‌های فعال GameLoop (Key: game_id)
        self.games: Dict[str, GameLoop] = {}
        # نقشه‌برداری سریع برای دسترسی با ID تلگرام (Key: user_id, Value: game_id)
        self.player_game: Dict[int, str] = {}

    async def create_game(self, p1_info: dict, p2_info: dict, market_id: str) -> GameLoop:

        # ۱. ساخت سشن در دیتابیس (Tortoise ORM یا هر مدلی که دارید)
        session = RoundSession(
            market_id=market_id,
            status=StatusEnum.in_progress,
            fsm_state="idle",
            game_data={} # داده‌های اولیه خالی
        )
        await session.insert()
        
        game_id = str(session.id)
        players = [p1_info, p2_info]

        # ۲. ایجاد نمونه GameLoop (حالا دیتای بازی داخل خودشه)
        game_instance = GameLoop(session, players)
        
        # ۳. انتقال به اولین وضعیت (waiting_strategy)
        await game_instance.start_game()

        # ۴. ثبت در سیستم مدیریت
        self.games[game_id] = game_instance
        for p in players:
            self.player_game[p["id"]] = game_id

        logging.info(f"Game {game_id} created and registered in RAM.")
        return game_instance

    def get_game(self, user_id: int) -> Optional[GameLoop]:
        """پیدا کردن شیء بازی بر اساس ID تلگرام کاربر"""
        game_id = self.player_game.get(user_id)
        if game_id:
            return self.games.get(game_id)
        return None

    async def end_game(self, game_id: str):
        """
        پاکسازی نهایی:
        1. تغییر وضعیت FSM به completed
        2. حذف از RAM
        """
        game = self.games.get(game_id)
        if not game:
            return

        # ۱. اتمام FSM (این کار باعث sync_db و ذخیره وضعیت نهایی می‌شود)
        await game.finish()

        # ۲. حذف دسترسی‌های سریع بازیکنان
        for p in game.players:
            self.player_game.pop(p["id"], None)

        # ۳. حذف از لیست بازی‌های فعال
        self.games.pop(game_id, None)
        logging.info(f"Game {game_id} has been terminated and cleaned up.")

# ایجاد یک نمونه واحد برای استفاده در کل پروژه
game_manager = GameManager()
