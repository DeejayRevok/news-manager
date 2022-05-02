from pypendency.argument import Argument
from pypendency.definition import Definition

from news_service_lib.configurable_container import ConfigurableContainer

from config import config


container: ConfigurableContainer = ConfigurableContainer([], config)


def load():
    container.set_definition(
        Definition(
            "apm",
            "elasticapm.Client",
            [
                Argument("transactions_ignore_patterns", ["^OPTIONS "]),
                Argument("service_name", "news-manager"),
                Argument("secret_token", "#elastic_apm.secret_token"),
                Argument("server_url", "#elastic_apm.url"),
            ],
        )
    )
    container.set_definition(
        Definition(
            "storage_client",
            "infrastructure.storage.mongo_storage_client.MongoStorageClient",
            [
                Argument.no_kw_argument("#mongo.members"),
                Argument.no_kw_argument("#mongo.rsname"),
                Argument.no_kw_argument("#mongo.database"),
            ],
        )
    )
    locker_type = config.server.locker
    container.set_definition(
        Definition(
            "locker",
            "infrastructure.locker.locker_factory",
            [Argument.no_kw_argument(locker_type), Argument.no_kw_argument(f"#{locker_type}")],
        )
    )
    container.set_definition(
        Definition("news_service", "services.news_service.NewsService", [Argument.no_kw_argument("@storage_client")])
    )
    container.set_definition(
        Definition(
            "uaa_service",
            "news_service_lib.uaa_service.UaaService",
            [
                Argument.no_kw_argument("#uaa.protocol"),
                Argument.no_kw_argument("#uaa.host"),
                Argument.no_kw_argument("#uaa.port"),
            ],
        )
    )
    container.set_definition(
        Definition(
            "nlp_service_service",
            "news_service_lib.nlp_service_service.NlpServiceService",
            [Argument("broker_config", "#rabbit"), Argument("redis_config", "#redis_nlp_worker")],
        )
    )
    container.set_definition(
        Definition(
            "news_consume_service",
            "services.news_consume_service.NewsConsumeService",
            [Argument.no_kw_argument("@news_service"), Argument.no_kw_argument("@nlp_service_service")],
        )
    )
    container.set_definition(
        Definition(
            "news_publish_service",
            "services.news_publish_service.NewsPublishService",
            [Argument.no_kw_argument("@news_service"), Argument.no_kw_argument("@locker")],
        )
    )
