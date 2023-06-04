"""
    Search module for searching the web based on user queries.
"""

import asyncio
from search_engine_parser.core.engines.yahoo import Search as YahooSearch


def searcher(query, n_results, n_pages, only_description):
    """
    Search the web using Yahoo Search engine and retrieve search results.

    Parameters:
        query : str
            The search query.

        n_results : int
            The number of search results to retrieve.

        n_pages : int
            The number of search result pages to crawl.

        only_description : bool
            If True, only retrieve the descriptions of the search results.
            If False, retrieve the titles, links, and descriptions of the search results.

    Returns:
        The search results.
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
            if only_description:
                results.append(f"|DESCRIPTIONS: {description}")
            else:
                results.append(
                    f"|TITLE: {title} LINK: {link} DESCRIPTIONS: {description}"
                )

    return results[:n_results]
