from typing import Any

from infrastructure.storage.filter.filter import Filter


class MatchFilter(Filter):
    parser_name = "parse_match"

    def __init__(self, key: Any, value: Any):
        super().__init__(key, value=value)
