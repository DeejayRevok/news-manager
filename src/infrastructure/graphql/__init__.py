from graphene import Schema
from pypendency.builder import container_builder

from infrastructure.graphql.queries import Query


def load() -> None:
    schema = Schema(query=Query)
    container_builder.set("graphene.Schema", schema)
