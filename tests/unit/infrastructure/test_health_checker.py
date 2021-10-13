from unittest import TestCase
from unittest.mock import Mock

from infrastructure.health_checker import NewsManagerHealthChecker
from infrastructure.storage.mongo_storage_client import MongoStorageClient


class TestHealthChecker(TestCase):
    def setUp(self) -> None:
        self.storage_client_mock = Mock(spec=MongoStorageClient)
        self.health_checker = NewsManagerHealthChecker(self.storage_client_mock)

    def test_health_check(self):
        test_health = True
        self.storage_client_mock.health_check.return_value = test_health

        health = self.health_checker.health_check()

        self.assertEqual(test_health, health)
