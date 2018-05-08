from algoliasearch_django import AlgoliaIndex

class SongIndex(AlgoliaIndex):
    should_index = 'should_index' # index only published songs
    fields = (
        "get_absolute_url", "title", "lyrics", "scripture_reference", "all_authors",
        )

    settings = {
        'searchableAttributes' : [
            "title", "lyrics", "scripture_reference", "all_authors",
            ],

        'attributesForFaceting' : ["title", "all_authors"],

        'queryType': 'prefixAll',
        'highlightPreTag': '<mark>',
        'highlightPostTag': '</mark>',
        'hitsPerPage': 20
    }