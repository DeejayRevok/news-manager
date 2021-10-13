from graphene import Schema

from webapp.graph.queries import Query

schema = Schema(query=Query)
