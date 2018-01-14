from django.apps import AppConfig
import algoliasearch_django as algoliasearch

from .index import PostIndex

class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        post = self.get_model("post")
        algoliasearch.register(post, PostIndex)
