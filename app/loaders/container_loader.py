from infrastructure import load as load_infrastructure
from application import load as load_application


def load():
    load_infrastructure()
    load_application()
