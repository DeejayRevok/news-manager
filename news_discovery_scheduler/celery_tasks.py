"""
News discovery celery app tasks definition module
"""
import json

from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from log_config import get_logger
from news_discovery_scheduler.celery_app import CELERY_APP
from news_discovery_scheduler.discovery.definitions import DEFINITIONS

LOGGER = get_logger()
QUEUE_PROVIDER_CONFIG = None


@CELERY_APP.app.task(name='initialize_worker')
def initialize_worker(broker_config: dict):
    """
    Initialize the celery worker global variables

    Args:
        broker_config: broker configuration

    """
    global QUEUE_PROVIDER_CONFIG
    LOGGER.info('Initializing worker')
    if QUEUE_PROVIDER_CONFIG is None:
        QUEUE_PROVIDER_CONFIG = broker_config
    else:
        LOGGER.info('Queue config already initialized')


@CELERY_APP.app.task(name='discover_news')
def discover_news(definition_name: str):
    """
    Discover news task

    Args:
        definition_name: name of the news discovery definition

    """
    global QUEUE_PROVIDER_CONFIG
    if QUEUE_PROVIDER_CONFIG:
        LOGGER.info(f'Executing discovery {definition_name}')
        definition = DEFINITIONS[definition_name]
        definition_instance = definition['class'](definition)
        connection = BlockingConnection(
            ConnectionParameters(host=QUEUE_PROVIDER_CONFIG['host'],
                                 port=int(QUEUE_PROVIDER_CONFIG['port']),
                                 credentials=PlainCredentials(QUEUE_PROVIDER_CONFIG['user'],
                                                              QUEUE_PROVIDER_CONFIG['password'])))
        channel = connection.channel()
        channel.exchange_declare(exchange='news-internal-exchange', exchange_type='fanout', durable=True)

        for discovered_new in definition_instance():
            channel.basic_publish(exchange='news-internal-exchange', routing_key='',
                                  body=json.dumps(dict(discovered_new)))
        channel.close()
        connection.close()
    else:
        LOGGER.error('Que provider not initialized, skipping discovery')
