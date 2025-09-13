import motor.motor_asyncio
from pymongo.errors import ServerSelectionTimeoutError

# MongoDB connection with proper limits
MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_DETAILS,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    socketTimeoutMS=10000,
    maxPoolSize=10,           # Limit connection pool
    minPoolSize=1,
    maxIdleTimeMS=30000,      # Close idle connections
    waitQueueTimeoutMS=5000,
)

database = client.assessment_db
employees_collection = database.get_collection("employees")

# Test connection with better error handling
async def test_mongodb_connection():
    try:
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        return True
    except ServerSelectionTimeoutError:
        print("❌ MongoDB connection failed: Server not reachable")
        return False
    except Exception as e:
        print(f"❌ Unexpected MongoDB error: {e}")
        return False