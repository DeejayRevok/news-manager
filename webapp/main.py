"""
Application main module
"""
from aiohttp.web_app import Application
from aiohttp_apispec import validation_middleware
from news_service_lib import HealthCheck, server_runner
from news_service_lib.graphql import setup_graphql_routes

from config import config, CONFIGS_PATH
from log_config import get_logger, LOG_CONFIG
from webapp.container_config import container, load
from webapp.definitions import health_check, API_VERSION
from webapp.graph import schema
from webapp.middlewares import error_middleware, uaa_auth_middleware
from webapp.views import news_view


async def shutdown(_):
    """
    Application shutdown handle
    """
    await container.get('news_consume_service').shutdown()
    await container.get('news_publish_service').shutdown()


def init_news_manager(app: Application) -> Application:
    """
    Initialize the web application

    Args:
        app: configuration profile to use

    Returns: web application initialized
    """
    load()
    container.get('locker').reset()
    container.get('news_consume_service')
    container.get('news_publish_service')
    HealthCheck(app, health_check)

    news_view.setup_routes(app)
    setup_graphql_routes(app, schema, get_logger())

    app.middlewares.append(error_middleware)
    app.middlewares.append(uaa_auth_middleware)
    app.middlewares.append(validation_middleware)

    app.on_shutdown.append(shutdown)

    return app


if __name__ == '__main__':
    server_runner('News manager', init_news_manager, API_VERSION, CONFIGS_PATH, config, LOG_CONFIG, get_logger)
