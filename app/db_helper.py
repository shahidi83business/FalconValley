# db_helper.py
from mongoengine import connect
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import asyncio

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "ecokirom"

client: AsyncIOMotorClient = None

async def connect_to_database():
    global client
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        await client.admin.command("ping")  # Check connection
        connect(DB_NAME)  # Connect to MongoEngine
        print(f"✅ Connected to MongoDB database: {DB_NAME}")
        return client[DB_NAME]
    except ConnectionFailure:
        print("❌ Failed to connect to MongoDB. Please check if MongoDB is running.")
        return None

async def disconnect_from_database():
    global client
    if client:
        client.close()
        print("🔌 Disconnected from MongoDB.")
