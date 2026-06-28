# session_service.py

from datetime import datetime
from app.data.models import RoundSession, User, Round, StatusEnum


async def create_round_session(user: User, round: Round) -> RoundSession:
    session = RoundSession(
        user=user,
        round=round,
        current_step=0,
        status=StatusEnum.in_progress,
        started_at=datetime.utcnow(),
    )
    await session.insert()
    return session
