from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiohttp_apispec import validation_middleware
from news_service_lib.graph.graphql_utils import setup_graphql_routes
from news_service_lib.healthcheck import setup_healthcheck
from news_service_lib.log_utils import add_logstash_handler
from news_service_lib.config_utils import load_config
from news_service_lib.api.utils import setup_swagger, setup_cors
from news_service_lib.server_utils import server_args_parser

from config import config
from log_config import get_logger, LOG_CONFIG
from webapp.container_config import container, load
from webapp.definitions import API_VERSION
from webapp.graph import schema
from webapp.middlewares import error_middleware, uaa_auth_middleware
from infrastructure.health_checker import NewsManagerHealthChecker
from webapp.views.news_view import NewsView


async def shutdown(_):
    await container.get("news_consume_service").shutdown()
    await container.get("news_publish_service").shutdown()


def init_news_manager() -> Application:
    app = Application()
    args = server_args_parser("News manager")
    loaded_config = load_config(args["configuration"], config, "NEWS_MANAGER")
    add_logstash_handler(LOG_CONFIG, config.logstash.host, config.logstash.port)
    load()

    app["host"] = loaded_config.server.host
    app["port"] = loaded_config.server.port

    container.get("locker").reset()
    container.get("news_consume_service")
    container.get("news_publish_service")
    setup_healthcheck(app, NewsManagerHealthChecker(container.get("storage_client")))

    NewsView(app, container.get("news_service"), get_logger())
    setup_graphql_routes(app, schema, get_logger())

    app.middlewares.append(error_middleware)
    app.middlewares.append(uaa_auth_middleware)
    app.middlewares.append(validation_middleware)

    app.on_shutdown.append(shutdown)

    server_base_path = config.server.base_path
    setup_swagger(app, server_base_path, API_VERSION)

    setup_cors(app)

    return app


if __name__ == "__main__":
    app = init_news_manager()
    run_app(app, host=app["host"], port=app["port"], access_log=get_logger())
