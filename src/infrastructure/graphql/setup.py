from aiohttp.abc import Application
from graphene import Schema
from graphql_server.aiohttp import GraphQLView


def setup_graphql_routes(app: Application, schema: Schema):
    __graphql_view_builder(
        app,
        route_path="/graphql",
        schema=schema,
        graphiql=False,
        enable_async=True,
    )


def __graphql_view_builder(app: Application, *, route_path="/graphql", route_name="graphql", **kwargs) -> None:
    view = GraphQLView(**kwargs)
    for method in "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD":
        app.router.add_route(method, route_path, view, name=route_name)

    if "graphiql" in kwargs and kwargs["graphiql"]:
        for method in "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD":
            app.router.add_route(method, "/graphiql", view, name="graphiql")
