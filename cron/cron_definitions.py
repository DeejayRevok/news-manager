"""
Cron definitions:
    class: cron implementation class
    expression: cron expression
    source_adapters: adapters used to get items
    **key_params: parameters required by the cron functionality
"""
from adapters.abc_rss_news_adapter import ABCRssNewsAdapter
from adapters.elconfidencial_rss_news_adapter import ConfidencialRssNewsAdapter
from cron.implementations.fetch_rss_news_implementation import FetchRssNewsImplementation

DEFINITIONS = {
    'fetch_rss_news': {
        'class': FetchRssNewsImplementation,
        'expression': '*/10 * * * *',
        'source_adapters': [ABCRssNewsAdapter, ConfidencialRssNewsAdapter],
        'abc_rss': 'https://www.abc.es/rss/feeds/abc_EspanaEspana.xml',
        'el_confidencial_rss': 'https://rss.elconfidencial.com/mundo/'
    }
}
