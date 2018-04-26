"""Tests"""

from random import choice

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

class SongIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for _ in range(26):
            mommy.make('song.Song', publish=True)
        for _ in range(25):
            mommy.make('song.Song', publish=False)

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

    def test_pagination_is_correct(self):
        resp = self.client.get(reverse('song:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['songs']) == 25)

    def test_all_published_songs_are_listed(self):
        resp = self.client.get(reverse('song:index') + "?page=2")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['songs']) == 1)

    def test_there_is_no_data_after_page_2(self):
        """Test that only songs with "publish=True" are in the view"""
        resp = self.client.get(reverse('song:index') + "?page=3")
        self.assertEqual(resp.status_code, 404)

class SongDetailViewTests(TestCase):
    def setUp(self):
        self.song = mommy.make('song.Song', title="some title", lyrics="Some lyrics")
    def tearDown(self):
        self.song.delete()

    def test_view_url_exists_at_desired_location(self):
        print('aaaaaaaa', self.song.pk)
        resp = self.client.get('/song/{}/{}'.format(self.song.pk, self.song.slug))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('song:detail', kwargs={'pk' : self.song.pk, 'slug' : self.song.slug}))
        print('ccccc', self.song.pk)
        self.assertEqual(resp.status_code, 200)

    def test_view_renders_correct_template(self):
        resp = self.client.get(reverse('song:detail', kwargs={'pk' : self.song.pk, 'slug' : self.song.slug}))
        self.assertEqual(resp.status_code, 200)
        print('bbbbb', self.song.pk)
        self.assertTemplateUsed(resp, 'song/detail.html')

    def test_view_has_correct_context(self):
        resp = self.client.get(reverse('song:detail', kwargs={'pk' : self.song.pk, 'slug' : self.song.slug}))
        print('eeee', self.song.pk)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('song' in resp.context)
        self.assertTrue('share_form' in resp.context)
