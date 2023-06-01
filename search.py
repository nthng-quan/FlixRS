from search_engine_parser.core.engines.yahoo import Search as YahooSearch


def search(query):
    results = []
    for i in range(1, 3):
        search_args = (query, i)
        ysearch = YahooSearch()
        yresults = ysearch.search(*search_args)

        for title, link, description in zip(
            yresults["titles"], yresults["links"], yresults["descriptions"]
        ):
            results.append(f"TITLE: {title} LINK: {link} DESCRIPTIONS: {description}")

    return results
