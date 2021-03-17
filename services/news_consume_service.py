"""
News consumer module
"""
import asyncio
import sys
from multiprocessing import Process
import json

from aiohttp.web_app import Application
from news_service_lib.messaging.exchange_consumer import ExchangeConsumer
from news_service_lib.models import New, NamedEntity

from log_config import get_logger

LOGGER = get_logger()


class NewsConsumeService:
    """
    News consumer service implementation
    """

    def __init__(self, app: Application):
        """
        Initialize the news consume service for the specified app

        Args:
            app: application associated
        """
        LOGGER.info('Starting news consumer service')
        self._app = app
        self._news_service = app['news_service']
        self._nlp_service_service = app['nlp_service_service']
        self._exchange_consumer = ExchangeConsumer(**app['config'].get_section('RABBIT'),
                                                   exchange='news-internal-exchange',
                                                   queue_name='news-exchange',
                                                   message_callback=self.handle_new,
                                                   logger=LOGGER)

        if not self._exchange_consumer.test_connection():
            LOGGER.error('Error connecting to the queue provider. Exiting...')
            sys.exit(1)

        self._consume_process = Process(target=self._exchange_consumer.__call__)
        self._consume_process.start()

    async def _handle_new(self, new: New):
        """
        Apply the new handling logic

        Args:
            new: new to handle

        """
        try:
            saved_new = await self._news_service.get_new_by_title(new.title)
        except KeyError:
            await self._news_service.save_new(new)
            saved_new = None

        if not saved_new or (saved_new and not saved_new.hydrated and not new.hydrated):
            try:
                await self._nlp_service_service.hydrate_new(new)
            except ConnectionError:
                LOGGER.warning('NLP service is not ready, skipping nlp hydrate')
            except ValueError:
                LOGGER.warning('JWT not configured, skipping nlp hydrate')
        elif saved_new and not saved_new.hydrated and new.hydrated:
            await self._news_service.save_new(new)

    def handle_new(self, _, __, ___, body: str):
        """
        Handle a new with the received data

        Args:
            body: message body with the new to handle

        """
        LOGGER.info('Handling new')
        self._app['apm'].client.begin_transaction('Consume')
        try:
            body = json.loads(body)
            new = New(title=body['title'],
                      url=body['url'],
                      content=body['content'],
                      source=body['source'],
                      date=body['date'],
                      hydrated=body['hydrated'],
                      summary=body['summary'],
                      sentiment=body['sentiment'],
                      entities=[NamedEntity(**entity) for entity in body['entities']],
                      noun_chunks=body['noun_chunks'])
            asyncio.run(self._handle_new(new))
            self._app['apm'].client.end_transaction('New handle', 'OK')
        except Exception as ex:
            LOGGER.error('Error while updating new %s', str(ex), exc_info=True)
            self._app['apm'].client.end_transaction('New handle', 'FAIL')
            self._app['apm'].client.capture_exception()

    async def shutdown(self):
        """
        Shutdown the news consumer service
        """
        LOGGER.info('Shutting down news consumer service')
        self._exchange_consumer.shutdown()
        self._consume_process.join()
