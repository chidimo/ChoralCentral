"""Tests"""

from django.test import TestCase
from django.shortcuts import reverse

from model_mommy import mommy

from .models import Author
from siteuser.models import CustomUser

class AuthorModelTests(TestCase):

    def setUp(self):
        self.author = mommy.make('author.Author')

    def test_model_representation(self):
        self.assertIsInstance(self.author, Author)
        self.assertEqual(
            self.author.__str__(), "{} {}".format(self.author.first_name, self.author.last_name))

    def test_absolute_url(self):
        abs_url = reverse('author:detail', kwargs={'pk' : self.author.pk, 'slug' : self.author.slug})
        self.assertEqual(self.author.get_absolute_url(), abs_url)

class AuthorIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for _ in range(35):
            mommy.make('author.Author')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/author/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('author:index'))
        self.assertEqual(resp.status_code, 200)

    def test_view_renders_correct_template(self):
        resp = self.client.get(reverse('author:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'author/index.html')

    def test_correct_pagination(self):
        resp = self.client.get(reverse('author:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['authors']) == 25)

    def test_that_all_authors_are_listed(self):
        resp = self.client.get(reverse('author:index')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['authors']) == 10)

class AuthorDetailViewTests(TestCase):

    def setUp(self):
        # set bio manually to avoid error being thrown by template tag markdown_format
        self.author = mommy.make('author.Author', bio='Some bio text')
        print('***pk:>>****', self.author.pk, '***slug:>>***', self.author.slug)

    def test_view_exists_at_desired_location(self):
        resp = self.client.get('/author/detail/{}/{}'.format(self.author.pk, self.author.slug))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('author:detail', kwargs={'pk' : self.author.pk, 'slug' : self.author.slug}))
        self.assertEqual(resp.status_code, 200)

    def test_view_renders_correct_template(self):
        resp = self.client.get(reverse('author:detail', kwargs={'pk' : self.author.pk, 'slug' : self.author.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'author/detail.html')

    def test_view_has_correct_context(self):
        resp = self.client.get(reverse('author:detail', kwargs={'pk' : self.author.pk, 'slug' : self.author.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('author' in resp.context)

class NewAuthorViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@user.app')
        self.user.is_active = True
        self.user.set_password("testpassword")
        self.user.save()

        # create a siteuser so the view doesn't throw an error on reversing siteuser detail
        self.siteuser = mommy.make(
            'siteuser.SiteUser', user=self.user, screen_name='screen_name')

    def test_redirects_if_not_logged_in(self):
        resp = self.client.get(reverse('author:new'))
        self.assertRedirects(resp, '/users/login/?next=/author/new/')

    def test_view_renders_correct_template(self):
        login = self.client.login(username='test@user.app', password='testpassword')
        resp = self.client.get(reverse('author:new'))
        self.assertEqual(resp.status_code, 200)

        # check user is logged in
        self.assertEqual(str(resp.context['user']), 'User - test@user.app')
        self.assertTemplateUsed(resp, 'author/new.html')

    def new_author_has_correct_creator(self): #selenium test?
        pass
