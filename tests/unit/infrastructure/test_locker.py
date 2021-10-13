from unittest import TestCase
from unittest.mock import patch

from infrastructure.locker import locker_factory, Locker
from infrastructure.locker.locker_type import LockerType


class TestLocker(TestCase):
    @patch("infrastructure.locker.redis_locker.BlockingConnectionPool")
    @patch("infrastructure.locker.redis_locker.Redis")
    def test_locker_factory_exists(self, _, __):
        locker_instance = locker_factory(LockerType.redis.name, dict(host="test", port="port", password=""))
        self.assertIsInstance(locker_instance, Locker)

    def test_locker_factory_not_exists(self):
        with self.assertRaises(NotImplementedError):
            locker_factory("NON_EXISTING_LOCKER_TYPE", {})
