
import os
from django.conf import settings
from django.core.files import File
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver

from .models import Score

@receiver(post_save, sender=Score)
def generate_pdf_preview(sender, instance, **kwargs):
    relative_media_path = instance.media_file.url
    full_media_path = settings.BASE_DIR + relative_media_path
    thumbnail_name = full_media_path.replace('.pdf', '')
    thumbnail_file = thumbnail_name + '.png'

    print("full path ", full_media_path)
    print("thumbnail ", thumbnail_name)
    print("thumbnail file ", thumbnail_file)

    # generate thumbnail
    cmd = "pdftoppm -png -f 1 -singlefile {} {}".format(full_media_path, thumbnail_name)
    os.system(cmd)

    try:
        content = File(open(thumbnail_file, "rb"))
        instance.thumbnail.save(instance.song.title + '.png', content, save=True)
        instance.save()
        os.remove(thumbnail_file)
    except FileNotFoundError:
        print("Probably windows system. File not generated")
        pass
