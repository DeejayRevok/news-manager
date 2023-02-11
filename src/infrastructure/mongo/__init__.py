from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.mongo.mongo_new_repository.MongoNewRepository",
            "infrastructure.mongo.mongo_new_repository.MongoNewRepository",
            [Argument.no_kw_argument("@pymongo.database.Database")],
        )
    )
