"""
News discovery celery beat module
"""
from celery.schedules import crontab
from elasticapm import Client
from elasticapm.contrib.celery import register_instrumentation, register_exception_tracking
from news_service_lib import profile_args_parser, add_logstash_handler
from news_service_lib.base_celery_app import BaseCeleryApp

from config import CONFIGS_PATH, config

from log_config import LOG_CONFIG, get_logger
from news_discovery_scheduler.discovery.definitions import DEFINITIONS
from news_discovery_scheduler.celery_tasks import discover_news
from news_service_lib.server_utils import load_config

CELERY_BEAT = BaseCeleryApp('News discovery app beat')
LOGGER = get_logger()


@CELERY_BEAT.app.on_after_configure.connect
def setup_periodic_tasks(sender, **__):
    """
    Set the periodic tasks for the current beat

    Args:
        sender: periodic task launcher
    """
    LOGGER.info('Configuring news discovery beat')
    for definition_key, definition_value in DEFINITIONS.items():
        cron_definition = definition_value['cron_expression'].split(' ')
        sender.add_periodic_task(crontab(*cron_definition), discover_news.s(definition_key), name=definition_key)


def main(profile: str):
    """
    Celery beat main entry point

    Args:
        profile: profile used to run the beat

    """
    load_config(profile, CONFIGS_PATH, config)

    add_logstash_handler(LOG_CONFIG, config.logstash.host, config.logstash.port)
    CELERY_BEAT.configure(task_queue_name='news-discovery',
                          broker_config=config.rabbit)

    apm_client = Client(config={
        'SERVICE_NAME': 'news-discovery-beat',
        'SECRET_TOKEN': config.elastic_apm.secret_token,
        'SERVER_URL': f'http://{config.elastic_apm.host}:{config.elastic_apm.port}'
    })
    register_instrumentation(apm_client)
    register_exception_tracking(apm_client)

    CELERY_BEAT.run(beat=True)


if __name__ == '__main__':
    args = profile_args_parser('News discovery beat application')
    main(args['profile'])
