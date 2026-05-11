from .decisions import decisions_bp
from .scenarios import scenarios_bp
from .auth import auth_bp
from .rounds import rounds_bp
from .sessions import sessions_bp
from .categories import categories_bp

ALL_BLUEPRINTS = [
    decisions_bp,
    scenarios_bp,
    auth_bp,
    categories_bp,
    rounds_bp,
    sessions_bp
]
