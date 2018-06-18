
import os
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Song

@receiver(post_save, sender=Song)
def reindex_songs_on_algolia(sender, instance, **kwargs):
    """Reindex songs when a song is saved only on production system"""

    if settings.SKIP_TASK is False:
        cmd = 'python manage.py algolia_reindex'
        os.system(cmd)
        print('Algolia index successfully update')
