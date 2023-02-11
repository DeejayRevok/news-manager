from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition

from infrastructure.api import load as load_api
from infrastructure.mongo import load as load_mongo
from infrastructure.graphql import load as load_graphql


def load() -> None:
    load_mongo()
    load_api()
    load_graphql()

    container_builder.set_definition(
        Definition(
            "infrastructure.health_checker.HealthChecker",
            "infrastructure.health_checker.HealthChecker",
            [Argument.no_kw_argument("@pymongo.MongoClient")],
        )
    )
