import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"  # change if needed

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.assessment_db  # DB name
employees_collection = database.get_collection("employees")
