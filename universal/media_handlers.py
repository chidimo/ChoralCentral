import os
from django.template.defaultfilters import slugify

def save_avatar(instance, filename):
    _, ext = os.path.splitext(filename)
    return "avatars/{}{}".format(instance.screen_name.lower(), ext)

def save_score_thumbnail(instance, filename):
    _, ext = os.path.splitext(filename)
    return "scorethumbnail/{}_{}_{}{}".format(
        instance.song.title.lower(),
        instance.part.name,
        instance.notation.name,
        ext)

def save_video_thumbnail(instance, filename):
    _, ext = os.path.splitext(filename)
    return "videothumbnails/{}{}".format(instance.screen_name.lower(), ext)

def save_midi(instance, filename):
    """Take the midi instance and original filename and return appropriate name"""
    filename, ext = os.path.splitext(filename)
    normalized_song_name = "_".join([each.lower() for each in instance.song.title.split()])
    normalized_song_name = slugify(instance.song.title)
    return "midis/{}_{}{}".format(normalized_song_name, instance.song.pk, ext)

def save_score(instance, filename):
    """Take the pdf instance and original filename and return appropriate name
    Append the Primary key to each file name so that names may not clash
    in case of multiple instance of same song title.
    """
    filename, ext = os.path.splitext(filename)
    normalized_song_name = slugify(instance.song.title)
    return "scores/{}_{}{}".format(normalized_song_name, instance.song.pk, ext)

