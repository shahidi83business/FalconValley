import os

APP_ENV = os.getenv("APP_ENV", "production")

if APP_ENV == "development":
    from .mock_ai import marketfactory
    from .mock_ai import scenario_engine
else:
    from .game import marketfactory
    from .game import scenario_engine

def get_market_factory(*args, **kwargs):
    return MarketFactory(*args, **kwargs)

def get_scenario_engine(*args, **kwargs):
    return ScenarioEngine(*args, **kwargs)
