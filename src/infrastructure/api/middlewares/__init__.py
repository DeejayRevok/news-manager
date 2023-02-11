from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.api.middlewares.error_middleware.ErrorMiddleware",
            "infrastructure.api.middlewares.error_middleware.ErrorMiddleware",
            [
                Argument.no_kw_argument("@logging.Logger"),
            ],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.api.middlewares.apm_middleware.APMMiddleware",
            "infrastructure.api.middlewares.apm_middleware.APMMiddleware",
            [
                Argument.no_kw_argument("@elasticapm.Client"),
            ],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.api.middlewares.log_middleware.LogMiddleware",
            "infrastructure.api.middlewares.log_middleware.LogMiddleware",
            [
                Argument.no_kw_argument("@logging.Logger"),
            ],
        )
    )
