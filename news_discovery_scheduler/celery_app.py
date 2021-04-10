"""
News discovery celery worker module
"""
from celery.concurrency import asynpool
from elasticapm import Client
from elasticapm.contrib.celery import register_instrumentation, register_exception_tracking

from news_service_lib import profile_args_parser, add_logstash_handler
from news_service_lib.base_celery_app import BaseCeleryApp
from news_service_lib.server_utils import load_config

from config import CONFIGS_PATH, config
from log_config import LOG_CONFIG, get_logger
from news_discovery_scheduler.container_config import load


asynpool.PROC_ALIVE_TIMEOUT = 60.0
CELERY_APP = BaseCeleryApp('News discovery app', ['news_discovery_scheduler.celery_tasks'])
LOGGER = get_logger()


def main(profile: str):
    """
    Celery app main entry point

    Args:
        profile: profile used to run the app

    """
    load_config(profile, CONFIGS_PATH, config)
    load()

    add_logstash_handler(LOG_CONFIG, config.logstash.host, config.logstash.port)
    CELERY_APP.configure(task_queue_name='news-discovery',
                         broker_config=config.rabbit,
                         worker_concurrency=config.celery.concurrency)

    apm_client = Client(config={
        'SERVICE_NAME': 'news-discovery-app',
        'SECRET_TOKEN': config.elastic_apm.secret_token,
        'SERVER_URL': config.elastic_apm.url
    })
    register_instrumentation(apm_client)
    register_exception_tracking(apm_client)

    CELERY_APP.run()


if __name__ == '__main__':
    args = profile_args_parser('News discovery application')
    main(args['profile'])
