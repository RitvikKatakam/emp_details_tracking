from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://127.0.0.1:27017/"
client = AsyncIOMotorClient(MONGO_URL)

db = client["employees_db"]
employees_collection = db["employeeinformation"]
