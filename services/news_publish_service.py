import sys
from dataclasses import asdict
from multiprocessing import Process

from news_service_lib.messaging.exchange_publisher import ExchangePublisher

from infrastructure.locker import Locker
from config import config
from log_config import get_logger
from services.news_service import NewsService

LOGGER = get_logger()


class NewsPublishService:
    def __init__(self, news_service: NewsService, locker_client: Locker):
        self._news_service = news_service
        self._locker_client = locker_client
        self._exchange_publisher = ExchangePublisher(**config.rabbit, exchange="news", logger=LOGGER)

        if not self._exchange_publisher.test_connection():
            LOGGER.error("Error connecting to the queue provider. Exiting...")
            sys.exit(1)

        self._publish_process = Process(target=self.__call__)
        self._publish_process.start()

    def __call__(self):
        self._exchange_publisher.connect()
        self._exchange_publisher.initialize()
        try:
            for storage_id, new_inserted in self._news_service.consume_new_inserts():
                LOGGER.info("Listened inserted new %s with id %s", new_inserted.title, storage_id)
                lock, lock_acquired = self._locker_client.acquire(storage_id, blocking=False)
                if lock_acquired:
                    self._exchange_publisher(asdict(new_inserted))
                    lock.release()
                else:
                    LOGGER.info("New stored with id %s already distributed", storage_id)
        except Exception as exc:
            LOGGER.error("Error while consuming from storage %s", str(exc))
        except KeyboardInterrupt:
            LOGGER.info("Request to stop listening for new updates in database")

    async def shutdown(self):
        self._publish_process.join()
        self._exchange_publisher.shutdown()
