from unittest import TestCase
from unittest.mock import patch

from infrastructure.locker.redis_locker import RedisLocker


class TestRedisLocker(TestCase):
    @patch("infrastructure.locker.redis_locker.BlockingConnectionPool")
    @patch("infrastructure.locker.redis_locker.Redis")
    def setUp(self, _, __) -> None:
        self._redis_locker = RedisLocker(host="test", port=1234, password="")

    @patch("infrastructure.locker.redis_locker.Lock")
    def test_acquiring_non_acquired(self, lock_mock):
        lock_mock().acquire.return_value = True
        lock, acquired = self._redis_locker.acquire("test")
        self.assertTrue(acquired)
        self.assertIsNotNone(lock)
        lock_mock.assert_called()

    @patch("infrastructure.locker.redis_locker.Lock")
    def test_acquiring_acquired(self, lock_mock):
        lock_mock().acquire.return_value = False
        lock, acquired = self._redis_locker.acquire("test")
        self.assertIsNotNone(lock)
        self.assertFalse(acquired)
        lock_mock.assert_called()
