from typing import Optional


class AsyncBaseManager:
    """Async base database manager class for database communication"""

    @property
    def client(self):
        """Client field to store database client object"""

        raise NotImplementedError('This field need to be defined into implementation class')

    @property
    def db(self):
        """DB field to store database connection object"""

        raise NotImplementedError('This field need to be defined into implementation class')

    async def connect_to_database(self, connection_string: str) -> None:
        """Method to define db field with connection to the database"""

        raise NotImplementedError('This method need to be defined into implementation class')

    async def close_database_connection(self) -> None:
        """Method to close database connection"""

        raise NotImplementedError('This method need to be defined into implementation class')

    async def is_file_parsed(self, file_name: str) -> bool:
        """Checks if provided file name was already parsed"""

        raise NotImplementedError('This method need to be defined into implementation class')

    async def save_parsed_file(self, file_name: str) -> None:
        """Save new parsed file in collection with parsed files"""

        raise NotImplementedError('This method need to be defined into implementation class')

    async def update_parsed_file(self, file_name: str) -> None:
        """Updates item by file name in collection with parsed files"""

        raise NotImplementedError('This method need to be defined into implementation class')

    async def delete_unparsed_files(self) -> None:
        """Delete all files with status field equals to 'STARTED' from collection with parsed files"""

        raise NotImplementedError('This method need to be defined into implementation class')

    async def save_trade_mark(self, trade_mark_data: dict) -> None:
        """Saves trade mark data"""

        raise NotImplementedError('This method need to be defined into implementation class')

    async def find_trade_mark(self, trade_mark_name: str) -> Optional[dict]:
        """Searches and returns trade mark data by variable trade_mark_name"""

        raise NotImplementedError('This method need to be defined into implementation class')

    async def find_nearest_trade_marks(self, trade_mark_name: str,
                                       limit: Optional[int]) -> list[Optional[dict]]:
        """Returns trade marks data by searching similar trade_mark_name

        :param trade_mark_name: name by which needs to find similar data
        :param limit: maximum number of results
        :return: list with found trade marks data
        """

        raise NotImplementedError('This method need to be defined into implementation class')
