"""
News discovery celery app tasks definition module
"""
from dataclasses import asdict

from celery.signals import worker_process_init, worker_process_shutdown

from news_discovery_scheduler.container_config import container
from news_service_lib.messaging import ExchangePublisher

from config import config
from log_config import get_logger
from news_discovery_scheduler.celery_app import CELERY_APP
from news_discovery_scheduler.discovery.definitions import DEFINITIONS

LOGGER = get_logger()


@worker_process_init.connect()
def initialize_worker(*_, **__):
    """
    Initialize the celery worker process environment
    """
    LOGGER.info('Initializing worker')
    exchange_publisher: ExchangePublisher = container.get('exchange_publisher')
    exchange_publisher.connect()
    exchange_publisher.initialize()


@CELERY_APP.app.task(name='discover_news')
def discover_news(definition_name: str):
    """
    Discover news task
    Args:
        definition_name: name of the news discovery definition
    """
    if 'rabbit' in config:
        LOGGER.info(f'Executing discovery {definition_name}')
        definition = DEFINITIONS[definition_name]
        definition_instance = definition['class'](definition)

        exchange_publisher: ExchangePublisher = container.get('exchange_publisher')

        for discovered_new in definition_instance():
            exchange_publisher(asdict(discovered_new))

    else:
        LOGGER.error('Worker configuration not initialized')


@worker_process_shutdown.connect()
def shutdown_worker(*_, **__):
    """
    Shutdown the celery worker shutting down the exchange publisher
    """
    LOGGER.info('Shutting down worker')
    exchange_publisher: ExchangePublisher = container.get('exchange_publisher')
    exchange_publisher.shutdown()
