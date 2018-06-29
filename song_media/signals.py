
import os
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Score, Midi

@receiver(post_save, sender=Score)
def backup_score_on_upload(sender, instance, **kwargs):
    """Backup scores"""

    if os.environ['DJANGO_SETTINGS_MODULE'] == 'choralcentral.settings.prod':
        os.system('source virtualenvwrapper.sh && workon __cc && python manage.py cc_backup_score')
        # os.system('python manage.py cc_backup_score')

@receiver(post_save, sender=Midi)
def backup_midi_on_upload(sender, instance, **kwargs):
    """Backup midi"""

    if os.environ['DJANGO_SETTINGS_MODULE'] == 'choralcentral.settings.prod':
        os.system('python manage.py cc_backup_midi')
