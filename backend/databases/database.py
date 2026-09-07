import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

mongoDB_url = os.getenv("MONGODB_URL")

client = AsyncIOMotorClient(mongoDB_url)

db = client.sereniq_db

users_collection = db.get_collection("users")

async def connected_to_mongoDB():
    try:
        await client.admin.command('ping')
        print("MongoDB server is live")
        return True
    except Exception as e:
        return {"message" : f"Error{e}"}


async def terminate_mongoDB():
    print("Closing Mongo DB connection")
    client.close()
    return {"message" : "MongoDB connection is closed"}
