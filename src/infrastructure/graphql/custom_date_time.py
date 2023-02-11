from datetime import datetime
from typing import Any

from graphene import Scalar, Node


class CustomDateTime(Scalar):
    @staticmethod
    def serialize(dt: Any) -> str:
        if not isinstance(dt, str):
            if isinstance(dt, float):
                return datetime.fromtimestamp(dt).isoformat()
            elif isinstance(dt, datetime):
                return dt.isoformat()
        else:
            return dt

    @staticmethod
    def parse_literal(node: Node) -> datetime:
        if isinstance(node.value, str):
            return datetime.fromisoformat(node.value)

    @staticmethod
    def parse_value(value: str) -> datetime:
        return datetime.fromisoformat(value)
