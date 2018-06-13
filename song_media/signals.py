
import os
from django.conf import settings
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Score

@receiver(post_save, sender=Score)
def generate_pdf_preview(sender, instance, **kwargs):
    relative_media_path = instance.media_file.url
    full_media_path = settings.BASE_DIR + relative_media_path
    thumbnail_name = full_media_path.replace('.pdf', '')
    thumbnail_file = thumbnail_name + '.png'

    if settings.SKIP_TASK is False:
        # generate thumbnail only in production system
        cmd = "pdftoppm -png -f 1 -singlefile {} {}".format(full_media_path, thumbnail_name)
        os.system(cmd)

    try:
        content = File(open(thumbnail_file, "rb"))
        # save=False avoids repeatedly triggering this signal
        instance.thumbnail.save(instance.song.title + '.png', content, save=False)
        os.remove(thumbnail_file)
    except FileNotFoundError:
        # print("Probably windows system. File not generated")
        pass
