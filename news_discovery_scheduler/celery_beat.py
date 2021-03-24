"""
News discovery celery beat module
"""
from celery.schedules import crontab
from elasticapm import Client
from elasticapm.contrib.celery import register_instrumentation, register_exception_tracking

from news_service_lib import profile_args_parser, Configuration, ConfigProfile, add_logstash_handler
from news_service_lib.base_celery_app import BaseCeleryApp

from news_discovery_scheduler.discovery.definitions import DEFINITIONS
from log_config import LOG_CONFIG, get_logger
from webapp.definitions import CONFIG_PATH
from news_discovery_scheduler.celery_tasks import discover_news


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


if __name__ == '__main__':
    ARGS = profile_args_parser('News discovery beat application')

    CONFIGURATION = Configuration(ConfigProfile[ARGS['profile']], CONFIG_PATH)
    add_logstash_handler(LOG_CONFIG, CONFIGURATION.get('LOGSTASH', 'host'), int(CONFIGURATION.get('LOGSTASH', 'port')))

    CELERY_BEAT.configure(task_queue_name='news-discovery',
                          broker_config=CONFIGURATION.get_section('RABBIT'))

    apm_client = Client(config={
        'SERVICE_NAME': 'news-discovery-beat',
        'SECRET_TOKEN': CONFIGURATION.get('ELASTIC_APM', 'secret-token'),
        'SERVER_URL': f'http://{CONFIGURATION.get("ELASTIC_APM", "host")}:{CONFIGURATION.get("ELASTIC_APM", "port")}'
    })
    register_instrumentation(apm_client)
    register_exception_tracking(apm_client)

    CELERY_BEAT.run(beat=True)
