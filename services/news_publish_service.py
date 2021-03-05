"""
News publish service module
"""
import sys
from multiprocessing import Process

from aiohttp.web_app import Application

from infrastructure.locker import Locker
from news_service_lib.messaging.exchange_publisher import ExchangePublisher

from log_config import get_logger
from services.news_service import NewsService

LOGGER = get_logger()


class NewsPublishService:
    """
    News publish service implementation
    """

    def __init__(self, app: Application):
        """
        Start a new process which listens the new inserts and publish them in the exchange configured

        Args:
            app: application associated
        """
        self._app = app
        self._news_service: NewsService = app['news_service']
        self._locker_client: Locker = app['locker_client']
        self._exchange_publisher = ExchangePublisher(**app['config'].get_section('RABBIT'), exchange='news',
                                                     logger=LOGGER)

        if not self._exchange_publisher.test_connection():
            LOGGER.error('Error connecting to the queue provider. Exiting...')
            sys.exit(1)

        self._publish_process = Process(target=self.__call__)
        self._publish_process.start()

    def __call__(self):
        """
        Initialize the exchange publisher and start listening the database inserts

        """
        self._exchange_publisher.connect()
        self._exchange_publisher.initialize()
        try:
            for storage_id, new_inserted in self._news_service.consume_new_inserts():
                LOGGER.info('Listened inserted new %s with id %s', new_inserted.title, storage_id)
                lock, lock_acquired = self._locker_client.acquire(storage_id, blocking=False)
                if lock_acquired:
                    self._exchange_publisher(dict(new_inserted))
                    lock.release()
                else:
                    LOGGER.info('New stored with id %s already distributed', storage_id)
        except Exception as exc:
            LOGGER.error('Error while consuming from storage %s', str(exc))
        except KeyboardInterrupt:
            LOGGER.info('Request to stop listening for new updates in database')

    async def shutdown(self):
        """
        Shutdown the current news publish service shutting down the exchange publisher and waiting the consume process
        to join
        """
        self._publish_process.join()
        self._exchange_publisher.shutdown()
