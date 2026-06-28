import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from beanie import init_beanie

from app.data.models import (
    Category,
    EconomyFunction,
    User,
    UserProfile,
    Market,
    Opponent,
    Scenario,
    Round,
    Decision,
    RoundSession,
    MetaData,
    EconomyState,
    Deal,
)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "ecokirom")

client: AsyncIOMotorClient | None = None
db = None
beanie_initialized = False


async def connect_to_database():
    global client, db, beanie_initialized

    try:
        if client is None:
            client = AsyncIOMotorClient(MONGO_URI)
            await client.admin.command("ping")
            db = client[DB_NAME]
        if not beanie_initialized:
            await init_beanie(
                database=db,
                document_models=[
                    Category,
                    EconomyFunction,
                    User,
                    UserProfile,
                    Market,
                    Opponent,
                    Scenario,
                    Round,
                    Decision,
                    RoundSession,
                    MetaData,
                    EconomyState,
                    Deal,
                ],
            )
            beanie_initialized = True

        print(f"✅ Connected to MongoDB database: {DB_NAME}")
        return db

    except ConnectionFailure:
        print("❌ Failed to connect to MongoDB. Please check if MongoDB is running.")
        return None


async def disconnect_from_database():
    global client, db, beanie_initialized

    if client:
        client.close()
        client = None
        db = None
        beanie_initialized = False
        print("🔌 Disconnected from MongoDB.")
