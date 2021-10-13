from enum import Enum

from infrastructure.locker.locker import Locker
from infrastructure.locker.redis_locker import RedisLocker


class LockerType(Enum):
    redis = RedisLocker

    def instance(self, **instance_config) -> Locker:
        return self.value(**instance_config)


def locker_factory(locker_type_name: str, locker_config) -> Locker:
    try:
        return LockerType[locker_type_name].instance(**locker_config)
    except KeyError:
        raise NotImplementedError(f"Locker type {locker_type_name} not implemented")
