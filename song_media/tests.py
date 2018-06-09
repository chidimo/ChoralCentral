from django.shortcuts import reverse
from django.test import TestCase

from model_mommy import mommy

from siteuser.models import CustomUser

class ScoreModelTests(TestCase):
    def setUp(self):
        uploader = mommy.make('siteuser.SiteUser')
        self.song = mommy.make('song.Song')
        self.part = mommy.make('song_media.VocalPart')
        self.notation = mommy.make('song_media.ScoreNotation')
        self.score = mommy.make('song_media.Score', uploader=uploader, media_file="some/file", song=self.song, part=self.part, notation=self.notation)

    def test_model_representation(self):
        rep = "{}-{}-{}".format(self.song.title, self.part , self.notation)
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

        mommy.make('siteuser.SiteUser', user=self.user, screen_name='screen_name')

        uploader = mommy.make('siteuser.SiteUser')
        self.song = mommy.make('song.Song')
        self.part = mommy.make('song_media.VocalPart')
        self.notation = mommy.make('song_media.ScoreNotation')
        data = {'song' : self.song, 'notation' : self.notation, 'part' : self.part, 'media_file' : "some/file"}

    def test_non_logged_in_user_cannot_access_new_score_page(self):
        url = reverse('song-media:score_add_song', kwargs={'pk' : self.song.pk})
        redirect_url = "/users/login/?next=/song-media/new-score/song-{}/".format(self.song.pk)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, redirect_url)

        login = self.client.login(username='test@user.app', password='testpassword')

        # test view is now accessible
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # check correct user is logged in
        self.assertEqual(str(resp.context['user']), 'User - test@user.app')
        self.assertTemplateUsed(resp, 'song_media/score_new.html')

        # post some data
        # self.client.post()
        
if __name__ == "__main__":
    unittest.main()
