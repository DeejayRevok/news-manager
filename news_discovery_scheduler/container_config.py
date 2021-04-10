"""
Application container configuration module
"""
from news_service_lib.configurable_container import ConfigurableContainer

from config import config
from log_config import get_logger
from news_service_lib.messaging import ExchangePublisher

container: ConfigurableContainer = ConfigurableContainer([], config)


def load():
    """
    Load all the application services in the container
    """
    container.set(
        "exchange_publisher",
        ExchangePublisher(**config.rabbit,
                          exchange='news-internal-exchange',
                          logger=get_logger())
    )


