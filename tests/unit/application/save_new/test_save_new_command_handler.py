from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

from bus_station.event_terminal.bus.event_bus import EventBus

from application.save_new.save_new_command import SaveNewCommand
from application.save_new.save_new_command_handler import SaveNewCommandHandler
from domain.new.named_entity import NamedEntity
from domain.new.new import New
from domain.new.new_repository import NewRepository
from domain.new.new_saved_event import NewSavedEvent


class TestSaveNewCommandHandler(TestCase):
    def setUp(self) -> None:
        self.new_repository_mock = Mock(spec=NewRepository)
        self.event_bus_mock = Mock(spec=EventBus)
        self.logger_mock = Mock(spec=Logger)
        self.command_handler = SaveNewCommandHandler(
            self.new_repository_mock,
            self.event_bus_mock,
            self.logger_mock
        )

    def test_handle_success(self):
        test_command = SaveNewCommand(
            title="test_new",
            url="test_new_url",
            content="test_new_content",
            source="test_new_source",
            date=323123112.0,
            language="test_new_language",
            hydrated=True,
            entities=[NamedEntity(text="test_named_entity", type="test_named_entity_type")],
            summary="test_new_summary",
            sentiment=1.23,
            image="test_image"
        )

        self.command_handler.handle(test_command)

        self.new_repository_mock.save.assert_called_once_with(
            New(
                title="test_new",
                url="test_new_url",
                content="test_new_content",
                source="test_new_source",
                date=323123112.0,
                language="test_new_language",
                hydrated=True,
                entities=[NamedEntity(text="test_named_entity", type="test_named_entity_type")],
                summary="test_new_summary",
                sentiment=1.23,
                image="test_image"
            )
        )
        self.event_bus_mock.transport.assert_called_once_with(
            NewSavedEvent(
                title="test_new",
                url="test_new_url",
                content="test_new_content",
                source="test_new_source",
                date=323123112.0,
                language="test_new_language",
                hydrated=True,
                entities=[NamedEntity(text="test_named_entity", type="test_named_entity_type")],
                summary="test_new_summary",
                sentiment=1.23,
                image="test_image"
            )
        )
