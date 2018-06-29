
import os
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Song

@receiver(post_save, sender=Song)
def reindex_songs_on_algolia(sender, instance, **kwargs):
    """Reindex songs when a song is saved only on production system"""

    if os.environ['DJANGO_SETTINGS_MODULE'] == 'choralcentral.settings.prod':
        os.system('python manage.py algolia_reindex')
