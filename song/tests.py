"""Tests"""
import unittest
from random import choice
from unittest import mock

from django.test import TestCase
from django.shortcuts import reverse

from model_mommy import mommy

from .models import Song#, Voicing, Language, Season, MassPart
from .models import Song

class VoicingModelTests(TestCase):
    def setUp(self):
        self.voicing = mommy.make('song.Voicing', voicing='satb')

    def test_model_representation(self):
        self.assertEqual(self.voicing.__str__(), 'satb')

    def test_absolute_url(self):
        self.assertEqual(self.voicing.get_absolute_url(), reverse('song:index'))

class LanguageModelTests(TestCase):
    def setUp(self):
        self.language = mommy.make('song.Language', language='igbo')

    def test_model_representation(self):
        self.assertEqual(self.language.__str__(), 'igbo')

    def test_absolute_url(self):
        self.assertEqual(self.language.get_absolute_url(), reverse('song:index'))

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

class SongIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        mommy.make('song.Song', publish=True, _quantity=27)
        mommy.make('song.Song', publish=False, _quantity=27)

    def test_total_songs_created(self):
        """Total number of songs created is 27+27=54"""
        songs = Song.objects.count()
        self.assertEqual(songs, 54)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('song:index'))
        self.assertEqual(resp.status_code, 200)

    def test_view_renders_correct_template(self):
        resp = self.client.get(reverse('song:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'song/index.html')

    def test_view_has_correct_context(self):
        resp = self.client.get(reverse('song:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('songs' in resp.context)
        self.assertTrue('form' in resp.context)

    def test_pagination(self):
        """Test pagination"""
        resp = self.client.get(reverse('song:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        # 25 songs on this page
        self.assertTrue(len(resp.context['songs']) == 25)

        # test page 2
        resp = self.client.get(reverse('song:index') + "?page=2")
        self.assertEqual(resp.status_code, 200)
        # only two songs on this page
        self.assertTrue(len(resp.context['songs']) == 2)

        # test page 3
        resp = self.client.get(reverse('song:index') + "?page=3")
        self.assertEqual(resp.status_code, 404)

class SongDetailViewTests(TestCase):
    def setUp(self):
        originator = mommy.make('siteuser.SiteUser')
        self.song = mommy.make('song.Song', originator=originator, title="some title", lyrics="Some lyrics")
    def tearDown(self):
        self.song.delete()

    def test_view_url_exists_at_desired_location(self):
        # resp = self.client.get('/song/{}/{}'.format(self.song.pk, self.song.slug))
        resp = self.client.get(reverse('song:detail', args=[self.song.pk, self.song.slug]))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('song:detail', kwargs={'pk' : self.song.pk, 'slug' : self.song.slug}))
        self.assertEqual(resp.status_code, 200)

    def test_view_renders_correct_template(self):
        resp = self.client.get(reverse('song:detail', kwargs={'pk' : self.song.pk, 'slug' : self.song.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'song/detail.html')

    def test_view_has_correct_context(self):
        resp = self.client.get(reverse('song:detail', kwargs={'pk' : self.song.pk, 'slug' : self.song.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('song' in resp.context)
        self.assertTrue('share_form' in resp.context)

if __name__ == "__main__":
    unittest.main()
