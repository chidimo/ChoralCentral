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
        self.voicing = mommy.make('song.Voicing', name='satb')

    def test_model(self):
        # model representation
        self.assertEqual(self.voicing.__str__(), 'satb')
        # absolute url
        self.assertEqual(self.voicing.get_absolute_url(), reverse('song:song_index'))

class LanguageModelTests(TestCase):
    def setUp(self):
        self.language = mommy.make('song.Language', name='igbo')

    def test_model(self):
        # model representation
        self.assertEqual(self.language.__str__(), 'igbo')
        # absolute url
        self.assertEqual(self.language.get_absolute_url(), reverse('song:song_index'))

class SongModelTests(TestCase):
    def setUp(self):
        creator = mommy.make('siteuser.SiteUser')
        self.song = mommy.make('song.Song', creator=creator, title='Some title', tempo=200)

    def test(self):
        self.assertIsInstance(self.song, Song)

        # model representation
        self.assertEqual(self.song.__str__(), self.song.title.title())

        abs_url = reverse('song:detail', kwargs={'pk' : self.song.pk, 'slug' : self.song.slug})
        self.assertEqual(self.song.get_absolute_url(), abs_url)

        # tempo text is set
        self.assertTrue(self.song.tempo_text)

        # test slug
        self.assertEqual(self.song.slug, 'some-title')

        # change title and test for slug
        self.song.title = 'Some new title'
        self.song.save()
        self.assertEqual(self.song.slug, 'some-new-title')

class SongIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        creator = mommy.make('siteuser.SiteUser')
        mommy.make('song.Song', creator=creator, publish=True, _quantity=22)
        mommy.make('song.Song', creator=creator, publish=False, _quantity=22)

    def test_view(self):
        self.assertEqual(Song.objects.count(), 44)

        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

        # url accessible by reverse
        resp = self.client.get(reverse('song:song_index'))
        self.assertEqual(resp.status_code, 200)

        # correct template rendered
        self.assertTemplateUsed(resp, 'song/index.html')

        # context
        self.assertTrue('songs' in resp.context)

        # pagination test
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        # 25 songs on this page
        self.assertTrue(len(resp.context['songs']) == 20)

        # test page 2
        resp = self.client.get(reverse('song:song_index') + "?page=2")
        self.assertEqual(resp.status_code, 200)
        # only two songs on this page
        self.assertTrue(len(resp.context['songs']) == 2)

        # test page 3
        resp = self.client.get(reverse('song:song_index') + "?page=3")
        self.assertEqual(resp.status_code, 404)

class SongDetailViewTests(TestCase):
    def setUp(self):
        creator = mommy.make('siteuser.SiteUser')
        self.song = mommy.make('song.Song', creator=creator, title="some title", lyrics="Some lyrics")
    def tearDown(self):
        self.song.delete()

    def test_detail_view(self):
        resp = self.client.get(reverse('song:detail', args=[self.song.pk, self.song.slug]))
        self.assertEqual(resp.status_code, 200)

        # url reversible
        resp = self.client.get(reverse('song:detail', kwargs={'pk' : self.song.pk, 'slug' : self.song.slug}))
        self.assertEqual(resp.status_code, 200)

        # renders correct template
        self.assertTemplateUsed(resp, 'song/detail.html')

        # renders expected context
        resp = self.client.get(reverse('song:detail', kwargs={'pk' : self.song.pk, 'slug' : self.song.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('song' in resp.context)
        self.assertTrue('share_form' in resp.context)

class SongFeedTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        creator = mommy.make('siteuser.SiteUser')
        mommy.make('song.Song', creator=creator, title="some title", lyrics="Some lyrics", publish=True, _quantity=27)
        mommy.make('song.Song', creator=creator, title="some title", lyrics="Some lyrics", publish=False, _quantity=27)

    def test_feed_url_reachable(self):
        url = reverse('song:song_feed', kwargs={'feed_type' : 'popular'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

if __name__ == "__main__":
    unittest.main()
