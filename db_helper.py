# db_connection.py
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import asyncio


MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "quizdb"

client: AsyncIOMotorClient = None
db = None


async def connect_to_database():
    global client, db

    try:
        client = AsyncIOMotorClient(MONGO_URI)
        # بررسی اتصال
        await client.admin.command("ping")
        db = client[DB_NAME]
        print(f"✅ Connected to MongoDB database: {DB_NAME}")
        return db

    except ConnectionFailure:
        print("❌ Failed to connect to MongoDB. Please check if MongoDB is running.")
        return None


async def disconnect_from_database():
    global client
    if client:
        client.close()
        print("🔌 Disconnected from MongoDB.")
