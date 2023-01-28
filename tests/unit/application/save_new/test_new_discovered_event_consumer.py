from unittest import TestCase
from unittest.mock import Mock

from bus_station.command_terminal.bus.command_bus import CommandBus

from application.save_new.new_discovered_event_consumer import NewDiscoveredEventConsumer
from application.save_new.save_new_command import SaveNewCommand
from domain.new.new import New
from domain.new.new_discovered_event import NewDiscoveredEvent
from domain.new.new_repository import NewRepository


class TestNewDiscoveredEventConsumer(TestCase):
    def setUp(self) -> None:
        self.new_repository_mock = Mock(spec=NewRepository)
        self.command_bus_mock = Mock(spec=CommandBus)
        self.event_consumer = NewDiscoveredEventConsumer(
            self.new_repository_mock,
            self.command_bus_mock
        )

    def test_consume_existing_new(self):
        test_new = New(
            title="test_title",
            url="test_url",
            content="test_content",
            source="test_source",
            date=2341231.23,
            language="test_language",
            hydrated=True
        )
        test_event = NewDiscoveredEvent(
            title="test_new",
            url="test_url",
            content="test_content",
            source="test_source",
            date=123123.45,
            language="test_language",
            image="test_image"
        )
        self.new_repository_mock.find_by_title.return_value = test_new

        self.event_consumer.consume(test_event)

        self.new_repository_mock.find_by_title.assert_called_once_with("test_new")
        self.command_bus_mock.transport.assert_not_called()

    def test_consume_non_existing_new(self):
        test_event = NewDiscoveredEvent(
            title="test_new",
            url="test_url",
            content="test_content",
            source="test_source",
            date=123123.45,
            language="test_language",
            image="test_image"
        )
        self.new_repository_mock.find_by_title.return_value = None

        self.event_consumer.consume(test_event)

        self.new_repository_mock.find_by_title.assert_called_once_with("test_new")
        self.command_bus_mock.transport.assert_called_once_with(
            SaveNewCommand(
                title="test_new",
                url="test_url",
                content="test_content",
                source="test_source",
                date=123123.45,
                language="test_language",
                image="test_image",
                hydrated=False,
                entities=[],
                sentiment=None,
                summary=None
        )
        )