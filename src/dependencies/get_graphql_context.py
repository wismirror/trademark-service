from fastapi import Depends

from src.db import get_database


async def get_graphql_context(database=Depends(get_database)):
    return {
        "database": database
    }
