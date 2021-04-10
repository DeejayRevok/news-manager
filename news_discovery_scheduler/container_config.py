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
        "exchange_publisher",
        "news_service_lib.messaging.ExchangePublisher",
        [
            Argument('host', '#rabbit.host'),
            Argument('port', '#rabbit.port'),
            Argument('user', '#rabbit.user'),
            Argument('password', '#rabbit.password'),
            Argument('exchange', 'news-internal-exchange'),
            Argument('logger', get_logger())
        ]
    )
    )


