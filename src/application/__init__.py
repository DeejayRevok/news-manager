from application.get_new import load as load_get_new
from application.get_news import load as load_get_news
from application.save_new import load as load_save_new


def load() -> None:
    load_get_new()
    load_get_news()
    load_save_new()
