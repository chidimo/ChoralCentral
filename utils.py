"""Utility functions available to all apps"""

# pylint: disable=C0326, C0301, C0103, C0111

from os.path import splitext
from random import randint, choices
from itertools import filterfalse
from django.conf import settings
from selenium.webdriver.support.select import Select

def fast_multiselect(driver, element_id, labels=[]):
    """https://sqa.stackexchange.com/questions/1355/what-is-
    the-correct-way-to-select-an-option-using-seleniums-python-webdriver"""
    select = Select(driver.find_element_by_id(element_id))

    if labels == []:
        texts = [opt.text for opt in select.options]
        labels = choices(texts, k=randint(1, len(texts)//2))

    for label in labels:
        select.select_by_visible_text(label)

def unique_everseen(iterable, key=None):
    """List unique elements, preserving order. Remember all elements ever seen.
    source: https://docs.python.org/3/library/itertools.html#itertools-recipes"""
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def upload_midi(instance, filename):
    """Take the midi instance and original filename and return appropriate name"""
    filename, ext = splitext(filename)
    normalized_song_name = "_".join([each.lower() for each in instance.song.title.split()])
    return "midis/{}_{}{}".format(normalized_song_name, instance.song.pk, ext)

def upload_pdf(instance, filename):
    """Take the pdf instance and original filename and return appropriate name
    I append the Primary key to each file name so that names may not clash
    in case of multiple instance of same song.
    """
    filename, ext = splitext(filename)
    normalized_song_name = "_".join([each.lower() for each in instance.song.title.split()])
    return "scores/{}_{}.{}".format(normalized_song_name, instance.song.pk, ext)


# def author_filter(author_object):
#     return author_object.name

# class AuthorsHomeView(generic.ListView):
#     template_name = "chinemerem/index.html"
#     context_object_name = 'authors'

#     def get_queryset(self): # remove duplicates
#         lyrs = Lyricist.objects.all()
#         comps = Composer.objects.all()
#         return sorted(unique_everseen(chain(lyrs, comps), key=author_filter), key=author_filter)
