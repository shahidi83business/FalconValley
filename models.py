
#enums
class StatusEnum(enum.Enum):
    in_progress = "in_progress"
    completed = "completed"
    abandoned = "abandoned"


class MetaParentType(enum.Enum):
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
    created_at = DateTimeField(default=now)
    updated_at = DateTimeField(default=now)

class Category(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    name = StringField(required=True)
    description = StringField()
    function = ReferenceField(EconomyFunction)
    created_at = DateTimeField(default=now)
    updated_at = DateTimeField(default=now)

class User(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    username = StringField(required=True, unique=True)
    created_at = DateTimeField(default=now)
    updated_at = DateTimeField(default=now)

class UserProfile(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    user = ReferenceField(User)
    created_at = DateTimeField(default=now)
    updated_at = DateTimeField(default=now)

class Opponent(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    strategy_key = StringField(required=True)
    parameters = DictField()
    created_at = DateTimeField(default=now)
    updated_at = DateTimeField(default=now)

class Scenario(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    text = StringField(required=True)
    options = ListField(StringField())
    correct_option = IntField(required=False, null=True)
    created_at = DateTimeField(default=now)
    updated_at = DateTimeField(default=now)

class Round(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    profile = ReferenceField(UserProfile)
    opponents = ReferenceField(Opponent)
    user = ReferenceField(User)
    category = ReferenceField(Category)
    created_at = DateTimeField(default=now)
    updated_at = DateTimeField(default=now)

class Decision(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    user = ReferenceField(User)
    scenario = ReferenceField(Scenario)
    selected_option = IntField(required=True)
    round = ReferenceField(Round)
    timestamp = DateTimeField(default=now)
    created_at = DateTimeField(default=now)
    updated_at = DateTimeField(default=now)

class RoundSession(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    user = ReferenceField(User)
    current_step = IntField(default=0)
    started_at = DateTimeField(default=now)
    ended_at = DateTimeField(required=False, null=True)
    status = EnumField(StatusEnum)
    round = ReferenceField(Round)
    created_at = DateTimeField(default=now)
    updated_at = DateTimeField(default=now)

class MetaData(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    parent_type = EnumField(MetaParentType)
    parent_id = StringField(required=True)
    key = StringField(required=True)
    value = DictField()
    created_at = DateTimeField(default=now)
    updated_at = DateTimeField(default=now)

