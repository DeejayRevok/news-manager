from unittest import TestCase
from unittest.mock import Mock

from bus_station.command_terminal.bus.command_bus import CommandBus

from application.save_new.new_hydrated_event_consumer import NewHydratedEventConsumer
from application.save_new.save_new_command import SaveNewCommand
from domain.new.new_hydrated_event import NewHydratedEvent


class TestNewHydratedEventConsumer(TestCase):
    def setUp(self) -> None:
        self.command_bus_mock = Mock(spec=CommandBus)
        self.event_consumer = NewHydratedEventConsumer(
            self.command_bus_mock
        )

    def test_consume_success(self):
        test_event = NewHydratedEvent(
            title="test_new",
            url="test_url",
            content="test_content",
            source="test_source",
            date=123123.45,
            language="test_language",
            image="test_image"
        )

        self.event_consumer.consume(test_event)

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
