from app.loaders.configuration_loader import load as load_configuration
from app.loaders.container_loader import load as load_container
from app.loaders.mongo_loader import load as load_mongo
from app.loaders.logger_loader import load as load_logger
from app.loaders.elastic_apm_loader import load as load_apm
from app.loaders.rabbitmq_connection_loader import load as load_rabbitmq
from app.loaders.redis_client_loader import load as load_redis
from app.loaders.buses import load as load_buses
from app.loaders.buses.command.handlers_registry import register as register_command_handlers
from app.loaders.buses.query.handlers_registry import register as register_query_handlers
from app.loaders.buses.event.consumers_registry import register as register_event_consumers
from app.loaders.buses.command.middlewares_loader import load as load_command_bus_middlewares
from app.loaders.buses.event.middlewares_loader import load as load_event_bus_middlewares
from app.loaders.buses.query.middlewares_loader import load as load_query_bus_middlewares


def load_app():
    load_configuration()
    load_logger()
    load_mongo()
    load_redis()
    load_rabbitmq()
    load_apm()
    load_container()
    load_buses()

    load_command_bus_middlewares()
    load_event_bus_middlewares()
    load_query_bus_middlewares()
    register_command_handlers()
    register_query_handlers()
    register_event_consumers()
