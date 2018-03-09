"""Test views"""

from django.test import TestCase
from django.shortcuts import reverse

from model_mommy import mommy 

class AuthorModelTests(TestCase):
    
    def setUp(self):
        self.author = mommy.make('author.Author')
    
    def test_model_representation(self):
        self.assertEqual(
            self.author.__str__(), "{} {}".format(self.author.first_name, self.author.last_name))

    def test_absolute_url(self):
        abs_url = reverse('author:detail', kwargs={'pk' : self.author.pk, 'slug' : self.author.slug})
        self.assertEqual(self.author.get_absolute_url(), abs_url)

