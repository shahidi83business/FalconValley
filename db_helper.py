# db_helper.py

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from beanie import init_beanie

from models import (
    Category,
    EconomyFunction,
    User,
    UserProfile,
    Opponent,
    Scenario,
    Round,
    Decision,
    RoundSession,
    MetaData,
    EconomyState,
)

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "ecokirom"

client: AsyncIOMotorClient | None = None
db = None


async def connect_to_database():
    global client, db

    if client is not None:
        return db

    try:
        client = AsyncIOMotorClient(MONGO_URI)

        # تست اتصال
        await client.admin.command("ping")

        db = client[DB_NAME]

        # initialize beanie
        await init_beanie(
            database=db,
            document_models=[
                Category,
                EconomyFunction,
                User,
                UserProfile,
                Opponent,
                Scenario,
                Round,
                Decision,
                RoundSession,
                MetaData,
                EconomyState,
            ],
        )

        print(f"✅ Connected to MongoDB database: {DB_NAME}")
        return db

    except ConnectionFailure:
        print("❌ Failed to connect to MongoDB. Please check if MongoDB is running.")
        return None


async def disconnect_from_database():
    global client

    if client:
        client.close()
        client = None
        print("🔌 Disconnected from MongoDB.")
