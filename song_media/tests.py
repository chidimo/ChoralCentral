import os.path
from io import BytesIO

from django.shortcuts import reverse
from django.test import TestCase
from django.conf import settings

from model_mommy import mommy

from siteuser.models import CustomUser

from .models import Score, ScoreNotation, VocalPart
from .forms import NewScoreForm

# class ScoreModelTests(TestCase):
#     def setUp(self):
#         self.creator = mommy.make('siteuser.SiteUser', pk=1)
#         self.song = mommy.make('song.Song')
#         self.part = mommy.make('song_media.VocalPart')
#         self.notation = mommy.make('song_media.ScoreNotation')
#         self.score = mommy.make('song_media.Score', creator=self.creator, media_file="some/file", song=self.song, part=self.part, notation=self.notation)

#     def tearDown(self):
#         self.creator.delete()
#         self.song.delete()
#         self.part.delete()
#         self.notation.delete()
#         self.score.delete()

#     def test_model_representation(self):
#         rep = "{}-{}-{}".format(self.song.title, self.part , self.notation)
#         self.assertEqual(self.score.__str__(), rep)

#     def test_absolute_url(self):
#         self.assertEqual(self.score.get_absolute_url(), reverse('song:detail', kwargs={'pk' : self.song.id, 'slug' : self.song.slug}))
    
# class NewScoreViewTests(TestCase):
#     def setUp(self):
#         # create a  user
#         self.user = CustomUser.objects.create_user(email='test@user.app')
#         self.user.is_active = True
#         self.user.set_password("testpassword")
#         self.user.save()

#         self.creator = mommy.make('siteuser.SiteUser', pk=1, user=self.user, screen_name='screen_name')
#         self.song = mommy.make('song.Song', title="Some title")
#         self.part = mommy.make('song_media.VocalPart', name="some name")
#         self.notation = mommy.make('song_media.ScoreNotation', name="some name")
#         self.score_count = Score.objects.count()

#     def tearDown(self):
#         self.user.delete()
#         self.creator.delete()
#         self.song.delete()
#         self.part.delete()
#         self.notation.delete()

#     def test_new_score_view(self):
#         url = reverse('song-media:score_add_to_song', kwargs={'pk' : self.song.pk})

#         # view redirects for anonymous user
#         resp = self.client.get(url)
#         redirect_url = "/users/login/?next=/song-media/new-score/song-{}/".format(self.song.pk)
#         self.assertEqual(resp.status_code, 302)
#         self.assertRedirects(resp, redirect_url)

#         login = self.client.login(username='test@user.app', password='testpassword')
#         resp = self.client.get(url)

#         # check url is reachable
#         self.assertEqual(resp.status_code, 200)
#         # check correct user is logged in
#         self.assertEqual(str(resp.context['user']), 'User - test@user.app')
#         # check template used
#         self.assertTemplateUsed(resp, 'song_media/score_new.html')
#         # check context
#         self.assertTrue('song' in resp.context)

#         # post data
#         score_data = {'notation' : self.notation, 'part' : self.part, 'media_file' : BytesIO(b'filepath')}
#         resp = self.client.post(reverse('song-media:score_add_to_song', kwargs={'pk' : self.song.pk}), score_data)

#         # assert view redirects        
#         self.assertEqual(resp.status_code, 302)
#         # assert author count has increased
#         self.assertEqual(Score.objects.count(), self.score_count+1)
#         # get created score
#         score = Score.objects.get(notation=self.notation, part=self.part)
#         # assert creator is logged in user
#         self.assertEqual(score.creator, self.creator)
#         # assert redirected to song detail url
#         self.assertEqual(resp['Location'], 'detail/{}/{}/'.format(self.song.pk, self.song.slug))

class NewScoreFormTests(TestCase):
    def setUp(self):
        # create a  user
        self.user = CustomUser.objects.create_user(email='test@user.app')
        self.user.is_active = True
        self.user.set_password("testpassword")
        self.user.save()

        self.creator = mommy.make('siteuser.SiteUser', pk=1, user=self.user, screen_name='screen_name')
        self.song = mommy.make('song.Song', title="Some title")
        self.part = mommy.make('song_media.VocalPart', name="Some name")
        self.notation = mommy.make('song_media.ScoreNotation', name="Some name")

    def test_valid_data(self):
        # file_path = os.path.join(settings.BASE_DIR, 'song_media', 'skills.pdf')
        # data = {'notation' : self.notation, 'part' : self.part, 'media_file' : open(file_path, 'rb')}
        data = {'notation' : self.notation, 'part' : self.part, 'media_file' : BytesIO(b'filepath')}

        form = NewScoreForm(data)
        self.assertTrue(form.is_valid())
        score = form.save()
        self.assertEqual(score.song.title, self.song.title)
        self.assertEqual(score.notation, self.notation)
        self.assertEqual(score.part, self.part)

        login = self.client.login(username='test@user.app', password='testpassword')

        data = {'notation' : self.notation, 'part' : self.part, 'media_file' : BytesIO(b'filepath')}
        form = NewScoreForm(data=data)
        self.assertTrue(form.is_valid())
        post_url = reverse('song-media:score_add_to_song', kwargs={'pk' : self.song.pk})
        resp = self.client.post(post_url, data)

        score = Score.objects.get(song=self.song, notation=self.notation, part=self.part)
        self.assertEqual(score.creator, self.creator)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], '/detail/{}/{}/'.format(score.song.pk, score.song.slug))

if __name__ == "__main__":
    unittest.main()
