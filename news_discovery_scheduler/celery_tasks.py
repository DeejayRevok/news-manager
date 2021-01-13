"""
News discovery celery app tasks definition module
"""
import os
from typing import Optional

from celery.signals import worker_process_init

from news_service_lib import ConfigProfile, Configuration
from news_service_lib.messaging import ExchangePublisher

from log_config import get_logger
from news_discovery_scheduler.celery_app import CELERY_APP
from news_discovery_scheduler.discovery.definitions import DEFINITIONS
from webapp.definitions import CONFIG_PATH

LOGGER = get_logger()
EXCHANGE_PUBLISHER: Optional[ExchangePublisher] = None


@worker_process_init.connect()
def initialize_worker(*_, **__):
    """
    Initialize the celery worker global variables
    """
    global EXCHANGE_PUBLISHER
    LOGGER.info('Initializing worker')

    config_profile = ConfigProfile[os.environ.get('PROFILE')] if 'PROFILE' in os.environ else ConfigProfile.LOCAL
    configuration = Configuration(config_profile, CONFIG_PATH)
    EXCHANGE_PUBLISHER = ExchangePublisher(**configuration.get_section('RABBIT'),
                                           exchange='news-internal-exchange',
                                           logger=LOGGER)
    EXCHANGE_PUBLISHER.connect()
    EXCHANGE_PUBLISHER.initialize()


@CELERY_APP.app.task(name='discover_news')
def discover_news(definition_name: str):
    """
    Discover news task

    Args:
        definition_name: name of the news discovery definition

    """
    global EXCHANGE_PUBLISHER
    if EXCHANGE_PUBLISHER:
        LOGGER.info(f'Executing discovery {definition_name}')
        definition = DEFINITIONS[definition_name]
        definition_instance = definition['class'](definition)

        for discovered_new in definition_instance():
            EXCHANGE_PUBLISHER(dict(discovered_new))
    else:
        LOGGER.error('Queue provider not initialized, skipping discovery')
