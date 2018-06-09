from django.test import TestCase

from model_mommy import mommy

class ScoreModelTests(TestCase):
    def setUp(self):
        uploader = mommy.make('siteuser.SiteUser')
        self.score = mommy.make(uploader=uploader, 'song_media.Score')
    
