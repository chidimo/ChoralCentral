from algoliasearch_django import AlgoliaIndex

class SongIndex(AlgoliaIndex):
    should_index = 'algolia_index_this' # index only published songs
    fields = (
        "get_absolute_url", "title", "lyrics", "genre", "ocassion", "all_authors",
        )

    settings = {
        'searchableAttributes' : [
            "title", "lyrics", "genre", "ocassion", "all_authors",
            ],

        'attributesForFaceting' : ["title", "all_authors", "genre", "ocassion"],

        'queryType': 'prefixAll',
        'highlightPreTag': '<mark>',
        'highlightPostTag': '</mark>',
        # 'hitsPerPage': 20,
        'paginationLimitedTo' : 0
    }
