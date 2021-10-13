from enum import Enum

import pymongo


class MongoSortDirection(Enum):
    ASC = pymongo.ASCENDING
    DESC = pymongo.DESCENDING
