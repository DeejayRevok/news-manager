"""
GraphQL queries entry point
"""
from webapp.graph.queries.news import NewsQuery


class Query(NewsQuery):
    """
    The main GraphQL query point.
    """
