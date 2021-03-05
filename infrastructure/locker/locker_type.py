"""
Locker type module
"""
from enum import Enum

from infrastructure.locker.locker import Locker
from infrastructure.locker.redis_locker import RedisLocker


class LockerType(Enum):
    """
    Locker types definition:
    - REDIS: Redis locker
    """
    REDIS = RedisLocker

    def instance(self, **instance_config) -> Locker:
        """
        Get the locker instance which corresponds to this type

        Args:
            **instance_config: instance configuration

        Returns: configured locker instance for this type

        """
        return self.value(**instance_config)


def locker_factory(locker_type_name: str, **locker_config) -> Locker:
    """
    Get the locker with the specified parameters

    Args:
        locker_type_name: name of the locker type to generate
        **locker_config: configuration for the locker

    Returns: configured locker instance

    """
    try:
        return LockerType[locker_type_name].instance(**locker_config)
    except KeyError:
        raise NotImplementedError(f'Locker type {locker_type_name} not implemented')
