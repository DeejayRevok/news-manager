from infrastructure.api.controllers import load as load_views
from infrastructure.api.middlewares import load as load_middlewares


def load() -> None:
    load_middlewares()
    load_views()
