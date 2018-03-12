
"""Views"""
import operator
from functools import reduce

import json
from django.conf import settings
from django.db.models import Count, Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin
from algoliasearch_django import get_adapter

from siteuser.models import SiteUser
from .models import Song
from author.models import Author

from .forms import ShareForm, NewSongForm, SongEditForm, SongFilterForm

from universal.utils import render_to_pdf

# pylint: disable=R0901, C0111

class InstantSong(PaginationMixin, generic.ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'song/instant_song.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(InstantSong, self).get_context_data(**kwargs)
        context['form'] = SongFilterForm()
        context['appID'] = settings.ALGOLIA['APPLICATION_ID']
        context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
        context['indexName'] = get_adapter(Song).index_name
        return context

def auto_song(request):
    context = {}
    context['appID'] = settings.ALGOLIA['APPLICATION_ID']
    context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
    context['indexName'] = get_adapter(Song).index_name
    return render(request, 'song/autocomplete_song.html', context)

# https://stackoverflow.com/questions/1960240/jquery-ajax-submit-form?rq=1
@login_required
@require_POST
def song_like_view(request):
    if request.method == 'POST':
        user = SiteUser.objects.get(user=request.user)
        pk = request.POST.get('pk', None)
        song = get_object_or_404(Song, pk=pk)

        if song.likes.filter(pk=user.pk).exists():
            song.likes.remove(user)
            song.save()
            message = "You unstarred this song.\n {} now has {} stars".format(song.title, song.like_count)
        else:
            song.likes.add(user)
            song.save()
            message = "You starred this song.\n {} now has {} stars".format(song.title, song.like_count)
    context = {'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

class SongLike(LoginRequiredMixin, View):
    def post(self):
        user = SiteUser.objects.get(user=self.request.user)
        song = get_object_or_404(Song, pk=self.request.POST.get('pk', None))

        if song.likes.filter(pk=user.pk).exists():
            song.likes.remove(user)
            song.save()
            message = "You unstarred this song.\n {} now has {} stars".format(song.title, song.like_count)
        else:
            song.likes.add(user)
            song.save()
            message = "You starred this song.\n {} now has {} stars".format(song.title, song.like_count)
        context = {'message' : message}
        return HttpResponse(json.dumps(context), content_type='application/json')

class SongIndex(PaginationMixin, generic.ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'song/index.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        # print("IP Address for debug-toolbar: " + self.request.META['REMOTE_ADDR'])
        context = super(SongIndex, self).get_context_data(**kwargs)
        context['form'] = SongFilterForm()
        # context['share_form'] = ShareForm()
        return context

class SongDetail(generic.DetailView):
    model = Song
    context_object_name = 'song'
    template_name = 'song/detail.html'

    def get_context_data(self, **kwargs):
        context = super(SongDetail, self).get_context_data(**kwargs)
        context['share_form'] = ShareForm()
        return context
    # add download incrementer here

class NewSong(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    template_name = 'song/new.html'
    form_class = NewSongForm

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)

        if (form.instance.first_line == "") and (form.instance.lyrics != ""):
            form.instance.first_line = form.instance.lyrics.split("\n")[0]
        self.object = form.save()
        self.object.likes.add(SiteUser.objects.get(user=self.request.user))
        messages.success(self.request, "Song was successfully added")
        return redirect(self.get_success_url())

class SongEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Song
    form_class = SongEditForm
    template_name = 'song/edit.html'
    success_message = "Song updated successfully"

class SongDelete(generic.DeleteView):
    model = Song
    success_url = reverse_lazy('song:index')
    template_name = "song/song_delete.html"

class FilterSongs(PaginationMixin, SuccessMessageMixin, generic.ListView):
    model = Song
    template_name = "song/index.html"
    context_object_name = "songs"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(FilterSongs, self).get_context_data(**kwargs)
        context['form'] = SongFilterForm()
        return context

    def get_queryset(self):
        if self.request.method == 'GET':
            form = SongFilterForm(self.request.GET)

            if form.is_valid():
                form = form.cleaned_data

                combinator = form['combinator']
                season = form['season']
                masspart = form['masspart']
                voicing = form["voicing"]
                language = form["language"]
                author = form['author']

                queries = []
                msg = []

                if author:
                    queries.append(Q(authors=author))
                    msg.append('Author={}'.format(author))
                if season:
                    queries.append(Q(seasons__season=season))
                    msg.append('Season={}'.format(season))
                if masspart:
                    queries.append(Q(mass_parts__part=masspart))
                    msg.append('Masspart={}'.format(masspart))
                if voicing:
                    queries.append(Q(voicing__voicing=voicing))
                    msg.append('Voicing={}'.format(voicing))
                if language:
                    queries.append(Q(language__language=language))
                    msg.append('Language={}'.format(language))

                if combinator == 'OR':
                    try:
                        query = reduce(operator.or_, queries)
                        query_str = " OR ".join(msg)
                    except TypeError:
                        query = []
                        # query_str = ""
                else:
                    try:
                        query = reduce(operator.and_, queries)
                        query_str = " AND ".join(msg)
                    except TypeError:
                        query = []
                        query_str = ""

                # execute query
                if query:
                    messages.success(self.request, "Search results for {}".format(query_str))
                    return Song.objects.filter(query)
                else:
                    messages.success(self.request, "You did not make any selection.")
                    return Song.published_set.all()

def reader_view(request, pk, slug):
    template = 'song/reader_view.html'
    song = Song.objects.get(pk=pk, slug=slug)
    context = {}
    context['song'] = song
    # return render(request, template, context)
    return render_to_pdf(request, template, context)

# https://www.webforefront.com/django/
def share_song_by_mail(request, pk, slug):
    context = {}

    from_email = settings.EMAIL_HOST_USER

    if request.method == 'GET':
        song = Song.objects.get(pk=pk, slug=slug)

        subject = '{} was shared with you from ChoralCentral'.format(song.title)
        context['song'] = song
        context['song_link'] = request.build_absolute_uri(song.get_absolute_url())

        form = ShareForm(request.GET)
        if form.is_valid():
            form = form.cleaned_data
            receiving_emails = form['receiving_emails']
            name = form['name']
            context['name'] = name

            email_list = [each.strip() for each in receiving_emails.split(',')]

            for email in email_list:
                text_email = render_to_string("song/share_song_by_mail.txt", context)
                html_email = render_to_string("song/share_song_by_mail.html", context)

                msg = EmailMultiAlternatives(subject, text_email, from_email, [email])
                msg.attach_alternative(html_email, "text/html")
                msg.send()

    success_msg = "Song was successfully sent to {}".format(", ".join(email_list))
    messages.success(request, success_msg)
    return redirect(song.get_absolute_url())

def share_on_facebook(request, pk, slug):
    pass




