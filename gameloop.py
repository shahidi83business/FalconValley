from transitions import Machine

class GameLoop:
    states = [
        'idle', 
        'entering_market',      # وضعیت جدید: در حال انتخاب/ورود به بازار
        'waiting_strategy', 
        'negotiation', 
        'decision', 
        'war_decision'
    ]

    def __init__(self, game_id):
        self.game_id = game_id
        self.machine = Machine(model=self, states=GameFSM.states, initial='idle')

        # جریان جدید:
        # ۱. شروع پروسه ورود
        self.machine.add_transition('start_entry', 'idle', 'entering_market')
        
        # ۲. رفتن به مرحله انتخاب استراتژی پس از موفقیت در ورود
        self.machine.add_transition('start_matching', 'entering_market', 'waiting_strategy')
        
        # جریان‌های قبلی بازی
        self.machine.add_transition('start_negotiation', 'waiting_strategy', 'negotiation')
        self.machine.add_transition('start_decision', ['waiting_strategy', 'negotiation'], 'decision')
        self.machine.add_transition('start_war', 'waiting_strategy', 'war_decision')
        self.machine.add_transition('finish', ['decision', 'war_decision'], 'idle')

    async def sync_db(self):
        """ذخیره وضعیت فعلی FSM در دیتابیس بیانی"""
        session = await RoundSession.get(self.session_id)
        if session:
            session.fsm_state = self.state  # ذخیره استیت فعلی (مثلا negotiation)
            
            # مدیریت وضعیت کلی
            if self.state == "idle":
                session.status = StatusEnum.completed
                session.ended_at = datetime.utcnow()
            else:
                session.status = StatusEnum.in_progress
                
            await session.save()
            print(f"DEBUG: Session {self.session_id} synced to state: {self.state}")
# --- Session Manager ساده برای GameLoop --- #

_game_sessions: dict[int, GameLoop] = {}


def get_game_session(game_id: int) -> GameLoop:
    """
    اگر برای این game_id قبلاً GameLoop ساخته شده باشد، همان را برمی‌گرداند،
    در غیر این صورت یکی جدید می‌سازد و ذخیره می‌کند.
    """
    if game_id not in _game_sessions:
        _game_sessions[game_id] = GameLoop(game_id)
    return _game_sessions[game_id]


def remove_game_session(game_id: int) -> None:
    """
    وقتی بازی تمام شد و از games حذفش کردی، این را هم صدا بزن
    تا FSM هم پاک شود.
    """
    _game_sessions.pop(game_id, None)
