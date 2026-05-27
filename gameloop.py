from transitions.extensions.asyncio import AsyncMachine
from models import RoundSession, StatusEnum
from engine import GameEngine

class GameLoop:
    def __init__(self, session: RoundSession, players_info: list):
        # ۱. دیتای بازی را همین‌جا ذخیره می‌کنیم
        self.session = session # دسترسی مستقیم به مدل دیتابیس
        self.game_id = str(session.id)
        self.players = players_info # [{id: 123, name: "Ali"}, ...]
        
        # دیتای عملیاتی بازی
        self.choices = {}
        self.strategy = {}
        self.war_choices = {}
        self.war_penalty = {p["id"]: 0 for p in players_info}
        self.market_id = session.market_id
        
        # ۲. تعریف وضعیت‌ها
        states = ['idle', 'waiting_strategy', 'waiting_negotiation', 'waiting_chicken', 'completed']
        
        self.machine = AsyncMachine(
            model=self, 
            states=states, 
            initial=session.fsm_state or 'idle',
            after_state_change='sync_db' # بعد از هر تغییر، دیتابیس آپدیت شود
        )

        # ۳. تعریف ترنزیشن‌ها
        self.machine.add_transition('start_game', 'idle', 'waiting_strategy')
        self.machine.add_transition('start_negotiation', 'waiting_strategy', 'waiting_negotiation')
        self.machine.add_transition('start_chicken', 'waiting_strategy', 'waiting_chicken')
        self.machine.add_transition('finish', '*', 'completed')

    async def sync_db(self):
        """ذخیره خودکار وضعیت در دیتابیس"""
        self.session.fsm_state = self.state
        
        # اگر بازی تمام شده، وضعیت کلی را هم آپدیت کن
        if self.state == 'completed':
            self.session.status = StatusEnum.completed
        
        # ذخیره متغیرهای بازی در فیلد game_data دیتابیس (برای Resume)
        self.session.game_data = {
            "choices": self.choices,
            "strategy": self.strategy,
            "war_choices": self.war_choices,
            "war_penalty": self.war_penalty
        }
        await self.session.save()

    # متدهای کمکی برای منطق بازی
    def is_everyone_ready(self, dict_name):
        target_dict = getattr(self, dict_name)
        return len(target_dict) == len(self.players)

    async def finalize(self):

        await self.finish()
