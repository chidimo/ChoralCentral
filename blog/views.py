"""Docstring"""

import json
from django import forms
from django.http import HttpResponseRedirect
from django.views import generic
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin
from algoliasearch_django import get_adapter

from siteuser.models import SiteUser
from song.models import Song
from .models import Post, Comment
from . import forms as fm

# pylint: disable=R0901, C0111

def instant_blog(request):
    context = {}
    context['appID'] = settings.ALGOLIA['APPLICATION_ID']
    context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
    context['indexName'] = get_adapter(Post).index_name
    context['posts'] = Post.published_set.all()
    return render(request, 'blog/instant_blog.html', context)

def auto_blog(request):
    context = {}
    context['appID'] = settings.ALGOLIA['APPLICATION_ID']
    context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
    context['indexName'] = get_adapter(Post).index_name
    return render(request, 'blog/autocomplete_blog.html', context)

class PostCreate(LoginRequiredMixin, generic.CreateView):
    context_object_name = 'post'
    template_name = 'blog/new.html'
    form_class = fm.NewPostForm

    def get_form_kwargs(self):
        """include 'user' and 'pk' in the kwargs to be sent to form"""
        kwargs = super(PostCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        print("********", self.request.user)
        return kwargs

    def form_valid(self, form):
        form.instance.creator = SiteUser.objects.get(user=self.request.user)
        return super(PostCreate, self).form_valid(form)

class PostCreateFromSong(LoginRequiredMixin, generic.CreateView):
    form_class = fm.PostCreateFromSongForm
    context_object_name = 'post'
    template_name = 'blog/new.html'

    def form_valid(self, form):
        form.instance.creator = SiteUser.objects.get(user=self.request.user)
        form.instance.song = Song.objects.get(pk=self.kwargs.get("pk", None))
        return super(PostCreateFromSong, self).form_valid(form)

class PostIndex(PaginationMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/index.html"
    paginate_by = 25

    def get_queryset(self):
        return Post.published_set.all()

    def get_context_data(self):
        context = super(PostIndex, self).get_context_data()
        context["search"] = fm.SearchForm
        return context

class PostDetail(PaginationMixin, generic.ListView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "comments"
    paginate_by = 15

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs.get("pk", None))
        return Comment.objects.filter(post=post)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context["comment_form"] = fm.CommentCreateForm()
        context["comment_number"] = fm.CommentNumberForm()
        context["post"] = Post.objects.get(pk=self.kwargs.get("pk", None))
        return context

class PostEdit(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = fm.PostEditForm
    template_name = "blog/edit.html"

class CommentCreate(LoginRequiredMixin, generic.CreateView):
    context_object_name = 'comment'
    form_class = fm.CommentCreateForm

    def form_valid(self, form):
        form.instance.creator = SiteUser.objects.get(user=self.request.user)
        form.instance.post = Post.objects.get(pk=self.kwargs.get("pk", None))
        return super(CommentCreate, self).form_valid(form)

class CommentEdit(LoginRequiredMixin, generic.CreateView):
    model = Comment
    context_object_name = 'comment'
    form_class = fm.CommentCreateForm
