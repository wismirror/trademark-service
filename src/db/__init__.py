from src.db.async_mongo_manager import AsyncMongoManager

db = AsyncMongoManager()


async def get_database() -> AsyncMongoManager:
    return db
