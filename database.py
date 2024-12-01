from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "test_database"
COLLECTION_NAME = "test_collection"

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        
    async def connect_to_mongo(self, uri_=MONGO_URI, db_=DATABASE_NAME, collection_=None):
        try:
            self.client = AsyncIOMotorClient(uri_)
            self.db = self.client[db_]
            if collection_:
                self.collection = self.db[collection_]
            await self.client.server_info()
            print("MongoDB 연결 성공")
        except ConnectionFailure as e:
            print(f"MongoDB 연결 실패: {e}")
        
    async def close_mongo_connection(self, ):
        if self.client:
            self.client.close()
            print("MongoDB 연결 해제")