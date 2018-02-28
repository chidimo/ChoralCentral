from os.path import splitext
from django.template.defaultfilters import slugify

def upload_midi(instance, filename):
    """Take the midi instance and original filename and return appropriate name"""
    filename, ext = splitext(filename)
    normalized_song_name = "_".join([each.lower() for each in instance.song.title.split()])
    normalized_song_name = slugify(instance.song.title)
    return "midis/{}_{}{}".format(normalized_song_name, instance.song.pk, ext)

def upload_pdf(instance, filename):
    """Take the pdf instance and original filename and return appropriate name
    Append the Primary key to each file name so that names may not clash
    in case of multiple instance of same song title.
    """
    filename, ext = splitext(filename)
    normalized_song_name = slugify(instance.song.title)
    return "scores/{}_{}.{}".format(normalized_song_name, instance.song.pk, ext)