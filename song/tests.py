"""Tests"""

from django.test import TestCase
from django.shortcuts import reverse

from model_mommy import mommy

# from .models import Voicing, Language, Season, MassPart, Song
from .models import Song
# from siteuser.models import CustomUser

class SongModelTests(TestCase):
    def setUp(self):
        self.song = mommy.make('song.Song', tempo=200)

    def test_model_representation(self):
        self.assertIsInstance(self.song, Song)
        self.assertEqual(self.song.__str__(), self.song.title)

    def test_absolute_url(self):
        abs_url = reverse('song:detail', kwargs={'pk' : self.song.pk, 'slug' : self.song.slug})
        self.assertEqual(self.song.get_absolute_url(), abs_url)

    def test_tempo_field_is_set(self):
        self.assertTrue(self.song.tempo_text)
