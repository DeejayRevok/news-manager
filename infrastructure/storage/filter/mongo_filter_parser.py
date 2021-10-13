from typing import Any


class MongoFilterParser:
    @staticmethod
    def parse_match(key: str, value: Any) -> dict:
        return {key: value}

    @staticmethod
    def parse_range(key: str, upper: Any = None, lower: Any = None) -> dict:
        range_query = {}
        if lower is not None:
            range_query["$gt"] = lower
        if upper is not None:
            range_query["$lt"] = upper
        return {key: range_query}
