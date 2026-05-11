from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    DictField,
    ReferenceField,
    ListField,
    IntField,
    BooleanField,
    EnumField,
)
from werkzeug.security import check_password_hash
from datetime import datetime
from enum import Enum
import uuid


def _now():
    return datetime.utcnow()


class StatusEnum(Enum):
    in_progress = "in_progress"
    completed = "completed"
    abandoned = "abandoned"


class MetaParentType(Enum):
    round_session = "round_session"
    decision = "decision"
    scenario = "scenario"
    user = "user"
    opponent = "opponent"


# Data models
class EconomyFunction(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    name = StringField(required=True)
    path = StringField()
    parameters = DictField()
    category = ReferenceField('Category')
    created_at = DateTimeField(default=_now)
    updated_at = DateTimeField(default=_now)


class Category(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    name = StringField(required=True)
    description = StringField()
    created_at = DateTimeField(default=_now)
    updated_at = DateTimeField(default=_now)


class User(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    username = StringField(required=False, unique=False)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=_now)
    updated_at = DateTimeField(default=_now)

    def check_password(self, raw_password):
        if not self.password:
            return False
        return check_password_hash(self.password, raw_password)


class UserProfile(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    user = ReferenceField(User)
    created_at = DateTimeField(default=_now)
    updated_at = DateTimeField(default=_now)


class Opponent(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    strategy_key = StringField(required=True)
    parameters = DictField()
    created_at = DateTimeField(default=_now)
    updated_at = DateTimeField(default=_now)


class Scenario(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    text = StringField(required=True)
    options = ListField(StringField())
    correct_option = IntField(required=False, null=True)
    created_at = DateTimeField(default=_now)
    updated_at = DateTimeField(default=_now)


class Round(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    profile = ReferenceField(UserProfile)
    opponents = ReferenceField(Opponent)
    user = ReferenceField(User)
    category = ReferenceField(Category)
    created_at = DateTimeField(default=_now)
    updated_at = DateTimeField(default=_now)


class Decision(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    user = ReferenceField(User)
    scenario = ReferenceField(Scenario)
    selected_option = IntField(required=True)
    round = ReferenceField(Round)
    timestamp = DateTimeField(default=_now)
    created_at = DateTimeField(default=_now)
    updated_at = DateTimeField(default=_now)


class RoundSession(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    user = ReferenceField(User)
    current_step = IntField(default=0)
    started_at = DateTimeField(default=_now)
    ended_at = DateTimeField(required=False, null=True)
    status = EnumField(StatusEnum)
    round = ReferenceField(Round)
    created_at = DateTimeField(default=_now)
    updated_at = DateTimeField(default=_now)


class MetaData(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    parent_type = EnumField(MetaParentType)
    parent_id = StringField(required=True)
    key = StringField(required=True)
    value = DictField()
    created_at = DateTimeField(default=_now)
    updated_at = DateTimeField(default=_now)

class EconomyState(Document):
    meta = {
        "collection": "economy_states",
        "indexes": [
            ("session", "round_number"),
            "-created_at"
        ],
        "ordering": ["round_number"]
    }

    # --- Relations ---
    session = ReferenceField(
        "RoundSession",
        required=True,
        reverse_delete_rule=2  # CASCADE
    )
    round_number = IntField(required=True, min_value=0)

    def to_dict(self):
        return {
            "id": str(self.id),
            "session_id": str(self.session.id),
        }