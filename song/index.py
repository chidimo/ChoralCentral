from algoliasearch_django import AlgoliaIndex

class SongIndex(AlgoliaIndex):
    algolia_indexable = 'algolia_indexable' # index only published songs
    fields = (
        "get_absolute_url", "title", "lyrics", "genre", "all_authors",
        )

    settings = {
        'searchableAttributes' : [
            "title", "lyrics", "genre", "all_authors",
            ],

        'attributesForFaceting' : ["title", "all_authors", "genre"],

        'queryType': 'prefixAll',
        'highlightPreTag': '<mark>',
        'highlightPostTag': '</mark>',
        'hitsPerPage': 20
    }