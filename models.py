#models.py
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
import uuid

from beanie import Document, Indexed, Link
from pydantic import Field


def _uuid_str() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.utcnow()


class StatusEnum(str, Enum):
    in_progress = "in_progress"
    completed = "completed"
    abandoned = "abandoned"


class MetaParentType(str, Enum):
    round_session = "round_session"
    decision = "decision"
    scenario = "scenario"
    user = "user"
    opponent = "opponent"


class BaseDoc(Document):
    id: str = Field(default_factory=_uuid_str)
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)

    async def save(self, *args, **kwargs):
        self.updated_at = _now()
        return await super().save(*args, **kwargs)


class Category(BaseDoc):
    name: str
    description: Optional[str] = None

    class Settings:
        name = "categories"


class EconomyFunction(BaseDoc):
    name: str
    path: Optional[str] = None
    parameters: Dict = Field(default_factory=dict)
    category: Optional[Link[Category]] = None

    class Settings:
        name = "economy_functions"


class User(BaseDoc):
    username: Optional[str] = None
    email: Indexed(str, unique=True)
    password: str

    class Settings:
        name = "users"


class UserProfile(BaseDoc):
    telegram_id: Indexed(int, unique=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None

    user: Optional[Link[User]] = None

    games: int = 0
    wins: int = 0
    loses: int = 0
    score: int = 0

    class Settings:
        name = "user_profiles"


class Opponent(BaseDoc):
    strategy_key: str
    parameters: Dict = Field(default_factory=dict)

    class Settings:
        name = "opponents"


class Scenario(BaseDoc):
    text: str
    options: List[str] = Field(default_factory=list)
    correct_option: Optional[int] = None

    class Settings:
        name = "scenarios"


class Round(BaseDoc):
    profile: Optional[Link[UserProfile]] = None
    opponents: Optional[Link[Opponent]] = None
    user: Optional[Link[User]] = None
    category: Optional[Link[Category]] = None

    class Settings:
        name = "rounds"


class Decision(BaseDoc):
    user: Optional[Link[User]] = None
    scenario: Optional[Link[Scenario]] = None
    selected_option: int
    round: Optional[Link[Round]] = None
    timestamp: datetime = Field(default_factory=_now)

    class Settings:
        name = "decisions"


class RoundSession(BaseDoc):
    user: Optional[Link[User]] = None
    current_step: int = 0
    started_at: datetime = Field(default_factory=_now)
    ended_at: Optional[datetime] = None
    status: StatusEnum
    round: Optional[Link[Round]] = None

    class Settings:
        name = "round_sessions"


class MetaData(BaseDoc):
    parent_type: MetaParentType
    parent_id: str
    key: str
    value: Dict = Field(default_factory=dict)

    class Settings:
        name = "metadata"


class EconomyState(BaseDoc):
    session: Link[RoundSession]
    round_number: int = Field(ge=0)

    class Settings:
        name = "economy_states"
        indexes = [
            [("session", 1), ("round_number", 1)],
            [("created_at", -1)],
        ]
