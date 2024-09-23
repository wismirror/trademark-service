from datetime import datetime
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import TEXT
from pymongo.errors import DuplicateKeyError

from src.core.settings import local as settings
from src.core.utils import get_trade_mark_field_name

from src.db.async_base_manager import AsyncBaseManager


class AsyncMongoManager(AsyncBaseManager):
    """Async database manager class to communicate with mongodb"""

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, connection_string: str):
        """Creates database connection"""

        self.client = AsyncIOMotorClient(
            connection_string,
            maxPoolSize=10,
            minPoolSize=10
        )
        self.db = self.client.root

    async def init_indexes(self) -> None:
        """Initializes mongodb text index for trade mark name field"""

        await self.db.trade_mark.create_index([(
            get_trade_mark_field_name(),
            TEXT
        )], default_language='english')

        await self.db.trade_mark.create_index(get_trade_mark_field_name(), unique=True)

    async def close_database_connection(self):
        """Close database connection"""

        self.client.close()

    async def is_file_parsed(self, file_name: str) -> bool:
        """Checks if provided file name was already parsed"""

        search_result = await self.db[settings.PARSED_FILE_COLLECTION].find_one({'file_name': file_name})
        return bool(search_result)

    async def save_parsed_file(self, file_name: str) -> None:
        """Save new parsed file in collection with parsed files"""

        await self.db[settings.PARSED_FILE_COLLECTION].insert_one({
            'file_name': file_name,
            'status': 'STARTED',
            'start_timestamp': int(datetime.now().timestamp())
        })

    async def update_parsed_file(self, file_name: str) -> None:
        """Updates item by file name in collection with parsed files"""

        await self.db[settings.PARSED_FILE_COLLECTION].update_one(
            filter={"file_name": file_name},
            update={
                "$set": {
                    "status": 'FINISHED',
                    "end_timestamp": int(datetime.now().timestamp())
                }
            }
        )

    async def delete_unparsed_files(self) -> None:
        """Delete all files with status field equals to 'STARTED' from collection with parsed files"""

        await self.db[settings.PARSED_FILE_COLLECTION].delete_many({
            'status': 'STARTED'
        })

    async def save_trade_mark(self, trade_mark_data: dict) -> None:
        """Saves trade mark data"""

        try:
            await self.db[settings.TRADE_MARK_COLLECTION].insert_one(trade_mark_data)
        except DuplicateKeyError:
            pass

    async def find_trade_mark(self, trade_mark_name: str) -> Optional[dict]:
        """Searches and returns trade mark data by variable trade_mark_name"""

        search_result = await self.db.trade_mark.find_one({
            get_trade_mark_field_name(): trade_mark_name
        })
        if search_result:
            return search_result

    async def find_nearest_trade_marks(self, trade_mark_name: str,
                                       limit: Optional[int]) -> list[Optional[dict]]:
        """Returns trade marks data by searching similar trade_mark_name

        :param trade_mark_name: name by which needs to find similar data
        :param limit: maximum number of results
        :return: list with found trade marks data
        """

        if limit is None:
            limit = 5
        else:
            assert limit > 0
        result = []
        async for trade_mark in self.db.trade_mark.find(
                {'$text': {'$search': trade_mark_name}},
                {'score': {'$meta': 'textScore'}}
        ).sort([('score', {'$meta': 'textScore'})]).limit(limit=limit):
            result.append(trade_mark)
        return result
