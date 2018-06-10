"""Tests"""

import unittest

from django.test import TestCase
from django.shortcuts import reverse

from model_mommy import mommy

from .models import Author
from .forms import NewAuthorForm
from siteuser.models import CustomUser

class AuthorModelTests(TestCase):

    def setUp(self):
        originator = mommy.make('siteuser.SiteUser')
        self.author = mommy.make('author.Author', originator=originator)

    def tearDown(self):
        self.author.delete()

    def test_model_representation(self):
        self.assertIsInstance(self.author, Author)
        self.assertEqual(
            self.author.__str__(), "{} {}".format(self.author.first_name, self.author.last_name))

    def test_absolute_url(self):
        abs_url = reverse('author:detail', kwargs={'pk' : self.author.pk, 'slug' : self.author.slug})
        self.assertEqual(self.author.get_absolute_url(), abs_url)

class AuthorIndexViewTests(TestCase):

    @classmethod    
    def setUpClass(cls):
        super(AuthorIndexViewTests, cls).setUpClass()
        originator = mommy.make('siteuser.SiteUser')
        for _ in range(35):
            mommy.make('author.Author', originator=originator)

    @classmethod
    def tearDownClass(cls):
        for each in Author.objects.all():
            each.delete()
        super(AuthorIndexViewTests, cls).tearDownClass()     

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
        originator = mommy.make('siteuser.SiteUser')
        self.author = mommy.make('author.Author', originator=originator, bio='Some bio text')

    def tearDown(self):
        self.author.delete()

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

        # create siteuser so the view doesn't throw an error on reversing siteuser detail present in the base url
        self.originator  = mommy.make('siteuser.SiteUser', user=self.user, screen_name='screen_name')
        self.author_count = Author.objects.count()

    def test_new_author_view(self):
        resp = self.client.get(reverse('author:new'))

        # assert view redirects for non-logged in user
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/users/login/?next=/author/new/')

        # login
        login = self.client.login(username='test@user.app', password='testpassword')
        
        # assert view accessible after log in
        resp = self.client.get(reverse('author:new'))
        self.assertEqual(resp.status_code, 200)

        # assert logged in user is correct
        self.assertEqual(str(resp.context['user']), 'User - test@user.app')
        self.assertTemplateUsed(resp, 'author/new.html')

        # create author
        author_data = {"author_type" : "lyricist", "first_name" : "first name", "last_name" : "last name", "bio" :"some random text"}
        resp = self.client.post('/author/new/', author_data)

        print("check the author pk", resp['Location'])

        # get created author
        author = Author.objects.get(first_name='first name', last_name='last name', author_type="lyricist")

        # assert new author has been created
        self.assertEqual(Author.objects.count(), self.author_count+1)
        
        # assert creator is logged in user
        self.assertEqual(author.originator, self.originator)

        # assert view redirects        
        self.assertEqual(resp.status_code, 302)

        # assert redirected to author detail url
        self.assertEqual(resp['Location'], '/author/detail/{}/{}'.format(author.pk, author.slug))

class NewAuthorFormTests(TestCase):
    def test_form(self):
        data = {"author_type" : "lyricist", "first_name" : "first name", "last_name" : "last name", "bio" :"some random text"}
        form = NewAuthorForm(data=data)
        self.assertTrue(form.is_valid())
