# session_service.py

from datetime import datetime
from models import RoundSession, User, Round, StatusEnum  # مسیرها را با کدت تنظیم کن


async def create_round_session(user: User, round: Round) -> RoundSession:
    session = RoundSession(
        user=user,
        round=round,
        current_step=0,
        status=StatusEnum.ACTIVE,   # یا هر نامی که در StatusEnum داری
        started_at=datetime.utcnow(),
    )
    await session.insert()
    return session
