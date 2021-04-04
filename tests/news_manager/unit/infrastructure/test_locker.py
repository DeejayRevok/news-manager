"""
Locker tests definition module
"""
from unittest import TestCase
from unittest.mock import patch

from infrastructure.locker import locker_factory, Locker
from infrastructure.locker.locker_type import LockerType


class TestLocker(TestCase):
    """
    Locker test cases implementation
    """
    @patch('infrastructure.locker.redis_locker.BlockingConnectionPool')
    @patch('infrastructure.locker.redis_locker.Redis')
    def test_locker_factory_exists(self, _, __):
        """
        Test if the specified locker exists the locker factory returns a Locker instance
        """
        locker_instance = locker_factory(LockerType.redis.name, host='test', port='port', password='')
        self.assertIsInstance(locker_instance, Locker)

    def test_locker_factory_not_exists(self):
        """
        Test if the specified locker not exists a NotImplementedError is raised
        """
        with self.assertRaises(NotImplementedError):
            locker_factory('NON_EXISTING_LOCKER_TYPE')
