"""
News discovery celery app tasks definition module
"""
import json

from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from config import config
from log_config import get_logger
from news_discovery_scheduler.celery_app import CELERY_APP
from news_discovery_scheduler.discovery.definitions import DEFINITIONS

LOGGER = get_logger()


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
        connection = BlockingConnection(
            ConnectionParameters(host=config.rabbit.host,
                                 port=config.rabbit.port,
                                 credentials=PlainCredentials(config.rabbit.user,
                                                              config.rabbit.password)))
        channel = connection.channel()
        channel.exchange_declare(exchange='news-internal-exchange', exchange_type='fanout', durable=True)

        for discovered_new in definition_instance():
            channel.basic_publish(exchange='news-internal-exchange', routing_key='',
                                  body=json.dumps(dict(discovered_new)))
        channel.close()
        connection.close()
    else:
        LOGGER.error('Worker configuration not initialized')
