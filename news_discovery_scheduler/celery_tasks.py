"""
News discovery celery app tasks definition module
"""
import json

from kombu import Exchange

from log_config import get_logger
from news_discovery_scheduler.celery_app import CELERY_APP
from news_discovery_scheduler.discovery.definitions import DEFINITIONS

LOGGER = get_logger()


@CELERY_APP.app.task
def discover_news(definition_name: str):
    """
    Discover news task

    Args:
        definition_name: name of the news discovery definition

    """
    LOGGER.info(f'Executing discovery {definition_name}')
    definition = DEFINITIONS[definition_name]
    definition_instance = definition['class'](definition)
    with CELERY_APP.app.pool.acquire(block=True) as conn:
        exchange = Exchange(name='news-internal-exchange', type='fanout', durable=True, channel=conn)
        exchange.declare()
        for discovered_new in definition_instance():
            exchange.publish(json.dumps(dict(discovered_new)))

