"""
    Search module for searching the web.
"""

import asyncio
from search_engine_parser.core.engines.yahoo import Search as YahooSearch

def searcher(query, n_results=5, n_pages=1):
    """
    docstring
    """
    results = []
    for i in range(1, n_pages + 1):
        search_args = (query, i)
        ysearch = YahooSearch()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        yresults = ysearch.search(*search_args)

        for title, link, description in zip(
            yresults["titles"], yresults["links"], yresults["descriptions"]
        ):
            results.append(f"TITLE: {title} LINK: {link} DESCRIPTIONS: {description}")

    return results[:n_results]
