import os

import aiohttp_cors
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_urldispatcher import StaticResource
from aiohttp_apispec import setup_aiohttp_apispec
from graphene import Schema
from yandil.container import default_container

from app.loaders import load_app
from infrastructure.api.controllers.get_news_controller import GetNewsController
from infrastructure.api.middlewares.apm_middleware import APMMiddleware
from infrastructure.api.middlewares.error_middleware import ErrorMiddleware
from infrastructure.api.middlewares.log_middleware import LogMiddleware
from infrastructure.graphql.queries import Query
from infrastructure.graphql.setup import setup_graphql_routes

API_VERSION = "1.0"


def load(*_) -> Application:
    load_app()
    app = Application()
    app["host"] = os.environ.get("NEWS_MANAGER_SERVER__HOST")
    app["port"] = os.environ.get("NEWS_MANAGER_SERVER__PORT")

    get_news_controller = default_container[GetNewsController]
    app.add_routes(
        [
            web.get(f"/api/{API_VERSION}/news", get_news_controller.get_news, allow_head=False),
        ]
    )

    graphql_scheme = Schema(query=Query)
    setup_graphql_routes(app, graphql_scheme)

    app.middlewares.append(default_container[ErrorMiddleware].middleware)
    app.middlewares.append(default_container[APMMiddleware].middleware)
    app.middlewares.append(default_container[LogMiddleware].middleware)

    setup_aiohttp_apispec(
        app=app,
        title="News manager API",
        version=API_VERSION,
        url=f"/api/{API_VERSION}/openapi.json",
        swagger_path=None,
        securityDefinitions={"ApiKeyAuth": {"type": "apiKey", "name": "X-API-Key", "in": "header"}},
    )
    __setup_cors(app)
    return app


def __setup_cors(app: Application):
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*", allow_methods="*"
            )
        },
    )
    for route in list(app.router.routes()):
        if not isinstance(route.resource, StaticResource):
            cors.add(route)
