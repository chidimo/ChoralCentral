from algoliasearch_django import AlgoliaIndex

class SongIndex(AlgoliaIndex):
    fields = (
        "get_absolute_url", "title", "lyrics", "scripture_ref", "all_authors", "all_seasons", "all_masspart"
        )

    settings = {
        'searchableAttributes' : [
            "title", "lyrics", "scripture_ref", "all_authors", "all_seasons", "all_masspart"
            ],

        'attributesForFaceting' : ["title", "all_authors", "all_seasons", "all_masspart"],

        'queryType': 'prefixAll',
        'highlightPreTag': '<mark>',
        'highlightPostTag': '</mark>',
        'hitsPerPage': 20
    }