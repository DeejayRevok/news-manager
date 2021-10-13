from unittest import TestCase

from infrastructure.storage.filter.mongo_filter_parser import MongoFilterParser


class TestMongoFilterParser(TestCase):
    def test_parse_match(self):
        parsed_filter = MongoFilterParser.parse_match("test", "test")
        self.assertEqual(parsed_filter, dict(test="test"))

    def test_parse_range(self):
        test_lower = 0
        test_upper = 2
        parsed_filter = MongoFilterParser.parse_range("test_int", upper=test_upper, lower=test_lower)
        self.assertEqual(parsed_filter, dict(test_int={"$gt": test_lower, "$lt": test_upper}))
