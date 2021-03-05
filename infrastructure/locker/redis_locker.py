"""
Redis locker module
"""
from typing import Tuple, Optional

import redis_lock
from redis import Redis, BlockingConnectionPool
from redis_lock import Lock

from infrastructure.locker.locker import Locker


class RedisLocker(Locker):
    """
    Redis locker implementation
    """

    def __init__(self, host: str, port: int, password: Optional[str]):
        """
        Initialize the redis locker with the provided redis configuration

        Args:
            host: redis service host address
            port: redis service port
            password: redis service access password
        """
        self._client = Redis(connection_pool=BlockingConnectionPool(host=host, port=port, password=password))

    def acquire(self, lock_name: str, blocking: bool = True) -> Tuple[Lock, bool]:
        lock = Lock(self._client, lock_name)
        return lock, lock.acquire(blocking=blocking)

    def release(self, lock: Lock):
        lock.release()

    def reset(self):
        redis_lock.reset_all(self._client)
