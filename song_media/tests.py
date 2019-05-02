import os.path
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from django.test import TestCase

from model_mommy import mommy

from siteuser.models import CustomUser

from song.models import Song

from .models import Score, ScoreNotation, VocalPart
from .forms import NewScoreForm

class ScoreModelTests(TestCase):
    def setUp(self):
        self.creator = mommy.make('siteuser.SiteUser', pk=1)
        self.song = mommy.make('song.Song')
        self.part = mommy.make('song_media.VocalPart')
        self.notation = mommy.make('song_media.ScoreNotation')
        self.score = mommy.make('song_media.Score', creator=self.creator, media_file="some/file", song=self.song, part=self.part, notation=self.notation)

    def tearDown(self):
        self.creator.delete()
        self.song.delete()
        self.part.delete()
        self.notation.delete()
        self.score.delete()

    def test_model_representation(self):
        rep = f"{self.song.title}-{self.part}-{self.notation}"
        self.assertEqual(self.score.__str__(), rep)

    def test_absolute_url(self):
        self.assertEqual(self.score.get_absolute_url(), reverse('song:detail', kwargs={'pk' : self.song.id, 'slug' : self.song.slug}))

class NewScoreViewTests(TestCase):
    def setUp(self):
        # create a  user
        self.user = CustomUser.objects.create_user(email='test@user.app')
        self.user.is_active = True
        self.user.set_password("testpassword")
        self.user.save()

        self.creator = mommy.make('siteuser.SiteUser', pk=1, user=self.user, screen_name='screen_name')
        self.song = mommy.make('song.Song', title="Some title")
        self.part = mommy.make('song_media.VocalPart', name="some name")
        self.notation = mommy.make('song_media.ScoreNotation', name="some name")
        self.score_count = Score.objects.count()

    def tearDown(self):
        self.user.delete()
        self.creator.delete()
        self.song.delete()
        self.part.delete()
        self.notation.delete()

    def test_new_score_view(self):
        url = reverse('song-media:score_add_to_song', kwargs={'pk' : self.song.pk})

        # view redirects for anonymous user
        resp = self.client.get(url)
        redirect_url = f"/users/login/?next=/song-media/new-score/song-{self.song.pk}/"
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, redirect_url)

        login = self.client.login(username='test@user.app', password='testpassword')
        resp = self.client.get(url)

        # check url is reachable
        self.assertEqual(resp.status_code, 200)
        # check correct user is logged in
        self.assertEqual(str(resp.context['user']), 'User - test@user.app')
        # check template used
        self.assertTemplateUsed(resp, 'song_media/score_new.html')
        # check context
        self.assertTrue('song' in resp.context)

        # post data
        media_file = MagicMock()
        data = {'notation' : self.notation, 'part' : self.part, 'media_file' : media_file}
        url = reverse('song-media:score_add_to_song', kwargs={'pk' : self.song.pk})
        resp = self.client.post(url, data)

        # assert view redirects
        self.assertEqual(resp.status_code, 302)
        # assert author count has increased
        self.assertEqual(Score.objects.count(), self.score_count+1)
        # get created score
        score = Score.objects.get(notation=self.notation, part=self.part)
        # assert creator is logged in user
        self.assertEqual(score.creator, self.creator)
        # assert redirected to song detail url
        self.assertEqual(resp['Location'], f'detail/{self.song.pk}/{self.song.slug}/')

class NewScoreFormTests(TestCase):
    def setUp(self):
        # create a  user
        self.user = CustomUser.objects.create_user(email='test@user.app')
        self.user.is_active = True
        self.user.set_password("testpassword")
        self.user.save()

        self.creator = mommy.make('siteuser.SiteUser', pk=1, user=self.user, screen_name='screen_name')

    def test_valid_data(self):
        part = mommy.make('song_media.VocalPart', name="Part name")
        notation = mommy.make('song_media.ScoreNotation', name="Notation name")
        
        # upload_file = open(Path(__file__).parent / 'skills.pdf', 'rb')
        # media_file = SimpleUploadedFile(upload_file.name, upload_file.read())
        
        media_file = MagicMock()
        media_file.size = 4 * 1024 * 1024 # increase size to test if error is thrown
        form = NewScoreForm({'notation' : notation.pk, 'part' : part.pk}, {'media_file': media_file})
        self.assertTrue(form.is_valid())

if __name__ == "__main__":
    unittest.main()
