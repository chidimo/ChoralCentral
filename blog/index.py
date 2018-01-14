from algoliasearch_django import AlgoliaIndex

class PostIndex(AlgoliaIndex):
    fields = (
        "get_absolute_url", "title", "subtitle", "body",
        )

    settings = {
        'searchableAttributes' : [
            "title", "subtitle", "body",
            ],

        'attributesForFaceting' : ["title", "subtitle", "body",],

        'queryType': 'prefixAll',
        'highlightPreTag': '<mark>',
        'highlightPostTag': '</mark>',
        'hitsPerPage': 20
    }