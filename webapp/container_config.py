"""
Application container configuration module
"""
from pypendency.argument import Argument
from pypendency.definition import Definition

from news_service_lib.configurable_container import ConfigurableContainer

from config import config
from log_config import get_logger


container: ConfigurableContainer = ConfigurableContainer([], config)


def load():
    """
    Load all the application services in the container
    """
    container.set_definition(Definition(
        "apm",
        "elasticapm.Client",
        [
            Argument('transactions_ignore_patterns', ['^OPTIONS ']),
            Argument('service_name', 'news-manager'),
            Argument('secret_token', '#elastic_apm.secret_token'),
            Argument('server_url', '#elastic_apm.url'),
        ]
    )
    )
    storage_type = config.server.storage
    container.set_definition(Definition(
        "storage_client",
        "news_service_lib.storage.storage_factory",
        [
            Argument.no_kw_argument(storage_type),
            Argument.no_kw_argument(f'#{storage_type}'),
            Argument.no_kw_argument(get_logger()),
        ]
    )
    )
    locker_type = config.server.locker
    container.set_definition(Definition(
        "locker",
        "infrastructure.locker.locker_factory",
        [
            Argument.no_kw_argument(locker_type),
            Argument.no_kw_argument(f'#{locker_type}')
        ]
    )
    )
    container.set_definition(Definition(
        "news_service",
        "services.news_service.NewsService",
        [
            Argument.no_kw_argument('@storage_client')
        ]
    )
    )
    container.set_definition(Definition(
        "uaa_service",
        "news_service_lib.uaa_service.get_uaa_service",
        [
            Argument.no_kw_argument('#uaa')
        ]
    )
    )
    container.set_definition(Definition(
        "nlp_service_service",
        "news_service_lib.NlpServiceService",
        [
            Argument('broker_config', '#rabbit'),
            Argument('redis_config', '#redis_nlp_worker')
        ]
    )
    )
    container.set_definition(Definition(
        "news_consume_service",
        "services.news_consume_service.NewsConsumeService",
        [
            Argument.no_kw_argument('@news_service'),
            Argument.no_kw_argument('@nlp_service_service')
        ]
    )
    )
    container.set_definition(Definition(
        "news_publish_service",
        "services.news_publish_service.NewsPublishService",
        [
            Argument.no_kw_argument('@news_service'),
            Argument.no_kw_argument('@locker')
        ]
    )
    )
