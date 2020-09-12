"""
Storage sorting types definitions module
"""
from enum import Enum

import pymongo


class SortDirection(Enum):
    """
    Storage results sorting type definition:
    - ASC = ascending sorting
    - DESC = descending sorting
    """
    ASC = [pymongo.ASCENDING]
    DESC = [pymongo.DESCENDING]
