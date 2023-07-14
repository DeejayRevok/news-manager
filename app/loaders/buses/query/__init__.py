from app.loaders.buses.query.sync_query_bus_loader import load as load_sync_query_bus
from app.loaders.buses.query.rpyc_query_bus_engine_components_loader import (
    load as load_rpyc_query_bus_engine_components,
)


def load() -> None:
    load_rpyc_query_bus_engine_components()
    load_sync_query_bus()
