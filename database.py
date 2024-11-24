from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

MONGO_URI = "mongodb://localhost:27017"  
DATABASE_NAME = "admin"                 

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

mongo = MongoDB()

# MongoDB 연결 함수
async def connect_to_mongo():
    try:
        mongo.client = AsyncIOMotorClient(MONGO_URI)
        mongo.db = mongo.client[DATABASE_NAME]
        print("MongoDB 연결 성공")
    except ConnectionFailure as e:
        print(f"MongoDB 연결 실패: {e}")

# MongoDB 연결 해제 함수
async def close_mongo_connection():
    if mongo.client:
        mongo.client.close()
        print("MongoDB 연결 해제")
