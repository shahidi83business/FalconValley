from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4


def new_id() -> str:
    return str(uuid4())


class BaseTimestampModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Scenario(BaseTimestampModel):
    id: str = Field(default_factory=new_id)
    text: str
    options: List[str]
    correct_option: Optional[int] = None


class User(BaseTimestampModel):
    id: str = Field(default_factory=new_id)
    username: str


class Decision(BaseTimestampModel):
    user_id: str
    scenario_id: str
    selected_option: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class DecisionSession(BaseTimestampModel):
    id: str = Field(default_factory=new_id)
    user_id: str
    current_step: int = 0
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    status: Literal["in_progress", "completed", "abandoned"] = "in_progress"


class DecisionMatrix(BaseTimestampModel):
    rows: List[Decision]
    profile_id: str
    category_id: str


class UserProfile(BaseTimestampModel):
    id: str = Field(default_factory=new_id)
    user_id: str


class Category(BaseTimestampModel):
    id: str = Field(default_factory=new_id)
    name: str
    description: str
    function_id: str


class Function(BaseTimestampModel):
    id: str = Field(default_factory=new_id)
    name: str
    path: str
    parameters: str
