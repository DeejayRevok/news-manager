"""
Application main module
"""
from aiohttp.web_app import Application
from aiohttp_apispec import validation_middleware
from news_service_lib import HealthCheck, server_runner, get_uaa_service, uaa_auth_middleware, initialize_apm, \
    NlpServiceService
from news_service_lib.graphql_utils import setup_graphql_routes
from news_service_lib.storage import storage_factory

from cron.cron_factory import initialize_crons
from log_config import get_logger, LOG_CONFIG
from services.news_consume_service import NewsConsumeService
from services.news_publish_service import NewsPublishService
from services.news_service import NewsService
from webapp.definitions import CONFIG_PATH, health_check, API_VERSION
from webapp.graph import schema
from webapp.middlewares import error_middleware
from webapp.views import news_view


async def shutdown(app: Application):
    """
    Application shutdown handle

    Args:
        app: application to shutdown
    """
    await app['news_consume_service'].shutdown()
    await app['news_publish_service'].shutdown()


def init_news_manager(app: Application) -> Application:
    """
    Initialize the web application

    Args:
        app: configuration profile to use

    Returns: web application initialized
    """

    storage_config = app['config'].get_section(app['config'].get('server', 'storage'))

    storage_client = storage_factory(app['config'].get('server', 'storage'), storage_config, get_logger())
    app['storage_client'] = storage_client

    app['news_service'] = NewsService(storage_client)

    uaa_config = app['config'].get_section('UAA')
    app['uaa_service'] = get_uaa_service(uaa_config)

    nlp_service_config = app['config'].get_section('NLP_SERVICE')
    app['nlp_service_service'] = NlpServiceService(**nlp_service_config)

    initialize_apm(app)

    app['news_consume_service'] = NewsConsumeService(app)
    app['news_publish_service'] = NewsPublishService(app)

    HealthCheck(app, health_check)

    news_view.setup_routes(app)
    setup_graphql_routes(app, schema, get_logger())

    app.middlewares.append(error_middleware)
    app.middlewares.append(uaa_auth_middleware)
    app.middlewares.append(validation_middleware)

    app.on_shutdown.append(shutdown)

    initialize_crons(app)

    return app


if __name__ == '__main__':
    server_runner('News manager', init_news_manager, API_VERSION, CONFIG_PATH, LOG_CONFIG, get_logger)
