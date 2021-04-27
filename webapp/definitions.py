"""
News manager webapp definitions module
"""
from news_service_lib.storage.mongo_utils import mongo_health_check

from webapp.container_config import container

API_VERSION = 'v1'


async def health_check() -> bool:
    """
    Check the health status of the application checking the connection with the database

    Returns: True if the status is OK, False otherwise

    """
    return mongo_health_check(container.get('storage_client')._mongo_client)
