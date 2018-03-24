import os
from django.template.defaultfilters import slugify

def upload_avatar(instance, filename):
    _, ext = os.path.splitext(filename)
    return "avatars/{}{}".format(instance.screen_name.lower(), ext)

def upload_video_thumbnail(instance, filename):
    _, ext = os.path.splitext(filename)
    return "thumbnails/{}{}".format(instance.screen_name.lower(), ext)

def upload_midi(instance, filename):
    """Take the midi instance and original filename and return appropriate name"""
    filename, ext = os.path.splitext(filename)
    normalized_song_name = "_".join([each.lower() for each in instance.song.title.split()])
    normalized_song_name = slugify(instance.song.title)
    return "midis/{}_{}{}".format(normalized_song_name, instance.song.pk, ext)

def upload_pdf(instance, filename):
    """Take the pdf instance and original filename and return appropriate name
    Append the Primary key to each file name so that names may not clash
    in case of multiple instance of same song title.
    """
    filename, ext = os.path.splitext(filename)
    normalized_song_name = slugify(instance.song.title)
    return "scores/{}_{}.{}".format(normalized_song_name, instance.song.pk, ext)
