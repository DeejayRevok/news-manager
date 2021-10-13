from typing import Tuple, Optional

import redis_lock
from redis import Redis, BlockingConnectionPool
from redis_lock import Lock

from infrastructure.locker.locker import Locker


class RedisLocker(Locker):
    def __init__(self, host: str, port: int, password: Optional[str]):
        self._client = Redis(connection_pool=BlockingConnectionPool(host=host, port=port, password=password))

    def acquire(self, lock_name: str, blocking: bool = True) -> Tuple[Lock, bool]:
        lock = Lock(self._client, lock_name)
        return lock, lock.acquire(blocking=blocking)

    def release(self, lock: Lock):
        lock.release()

    def reset(self):
        redis_lock.reset_all(self._client)
