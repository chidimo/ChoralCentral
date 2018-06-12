
import os
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Song

@receiver(post_save, sender=Song)
def reindex_songs_on_algolia(sender, instance, **kwargs):
    """Reindex songs when a song is saved only on production system"""
    print("Running signal")

    if settings.DEBUG is False:
        cmd = 'python manage.py algolia_reindex'
        os.system(cmd)
        print('Algolia index successfully update')
