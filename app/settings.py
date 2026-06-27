# app/config/settings.py

import os
from dotenv import load_dotenv


APP_ENV = os.getenv("APP_ENV", "dev")

env_file = {
    "dev": ".env.dev",
    "prod": ".env.prod",
}.get(APP_ENV, ".env.dev")

load_dotenv(env_file)


class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "dev")

    # Telegram
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    BASE_URL: str = os.getenv("BASE_URL", "https://api.telegram.org/bot")

    # Database
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "falcon_valley_dev")

    # AI
    AI_MODE: str = os.getenv("AI_MODE", "mock")  
    # mock | real

    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai")
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")

    # Runtime
    ENABLE_SCHEDULER: bool = os.getenv("ENABLE_SCHEDULER", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @property
    def telegram_bot_url(self) -> str:
        return f"{self.BASE_URL}{self.BOT_TOKEN}"


settings = Settings()
