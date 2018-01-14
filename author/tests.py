"""Test views"""

from django.test import TestCase
from django.shortcuts import reverse

class AuthorViewTest(TestCase):
    fixtures = ["fixtures/siteusers.json", "fixtures/authors.json",]

    def test_index(self):
        resp = self.client.get("/author/index/")
        self.assertEqual(resp.status_code, 200)
