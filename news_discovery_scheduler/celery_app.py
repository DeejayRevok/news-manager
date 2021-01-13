"""
News discovery celery worker module
"""
from celery.concurrency import asynpool

from news_service_lib import profile_args_parser, Configuration, ConfigProfile, add_logstash_handler
from news_service_lib.base_celery_app import BaseCeleryApp

from log_config import LOG_CONFIG, get_logger
from webapp.definitions import CONFIG_PATH


asynpool.PROC_ALIVE_TIMEOUT = 60.0
CELERY_APP = BaseCeleryApp('News discovery app', ['news_discovery_scheduler.celery_tasks'])
LOGGER = get_logger()


if __name__ == '__main__':
    ARGS = profile_args_parser('News discovery application')

    CONFIGURATION = Configuration(ConfigProfile[ARGS['profile']], CONFIG_PATH)
    add_logstash_handler(LOG_CONFIG, CONFIGURATION.get('LOGSTASH', 'host'), int(CONFIGURATION.get('LOGSTASH', 'port')))
    CELERY_APP.configure(task_queue_name='news-discovery',
                         broker_config=CONFIGURATION.get_section('RABBIT'),
                         worker_concurrency=int(CONFIGURATION.get('CELERY', 'concurrency')))
    CELERY_APP.run()
