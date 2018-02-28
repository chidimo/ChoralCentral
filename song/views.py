
"""Views"""
import operator
from functools import reduce

import json
from django.conf import settings
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import generic
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

from .forms import NewSongForm, SongEditForm, SongFilterForm

from universal.utils import render_to_pdf

# pylint: disable=R0901, C0111

def instant_song(request):
    context = {}
    context['appID'] = settings.ALGOLIA['APPLICATION_ID']
    context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
    context['indexName'] = get_adapter(Song).index_name

    context['is_paginated'] = True
    return render(request, 'song/instant_song.html', context)

def auto_song(request):
    context = {}
    context['appID'] = settings.ALGOLIA['APPLICATION_ID']
    context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
    context['indexName'] = get_adapter(Song).index_name
    return render(request, 'song/autocomplete_song.html', context)

@login_required
@require_POST
def song_like_view(request):
    if request.method == 'POST':
        user = SiteUser.objects.get(user=request.user)
        song = get_object_or_404(Song, id=request.POST.get('pk', None))

        if song.likes.filter(id=user.id).exists():
            song.likes.remove(user)
            song.like_count -= 1
            song.save()
            message = "You unstarred this song"
        else:
            song.likes.add(user)
            song.like_count += 1
            song.save()
            message = "You starred this song"
    context = {'like_count' : song.like_count, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

class SongIndex(PaginationMixin, generic.ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'song/index.html'
    # paginate_by = 50

    def get_context_data(self, **kwargs):
        # print("IP Address for debug-toolbar: " + self.request.META['REMOTE_ADDR'])
        context = super(SongIndex, self).get_context_data(**kwargs)
        context['form'] = SongFilterForm()
        return context

class SongDetail(generic.DetailView):
    model = Song
    context_object_name = 'song'
    template_name = 'song/detail.html'

    # add download incrementer here

def reader_view(request, pk, slug):
    template = 'song/reader_view.html'
    song = Song.objects.get(pk=pk, slug=slug)
    context = {}
    context['song'] = song
    return render_to_pdf(request, template, context)

class NewSong(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    template_name = 'song/new.html'
    form_class = NewSongForm

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)

        if (form.instance.first_line == "") and (form.instance.lyrics != ""):
            form.instance.first_line = form.instance.lyrics.split("\n")[0]
        self.object = form.save()
        self.object.likes.add(SiteUser.objects.get(user=self.request.user))
        return redirect(self.get_success_url())

class SongEdit(LoginRequiredMixin, generic.UpdateView):
    model = Song
    form_class = SongEditForm
    template_name = 'song/edit.html'

class SongDelete(generic.DeleteView):
    model = Song
    success_url = reverse_lazy('song:index')
    template_name = "song/song_delete.html"

    def get_context_data(self, **kwargs):
        context = super(SongDelete, self).get_context_data(**kwargs)
        context["which_model"] = "Song"
        return context

def filter_songs(request):
    template = "song/index.html"
    if request.GET:
        form = SongFilterForm(request.GET)
        if form.is_valid():
            form = form.cleaned_data

            combinator = form['combinator']
            season = form['season']
            masspart = form['masspart']
            voicing = form["voicing"]
            language = form["language"]

            queries = []
            msg = []

            if season:
                queries.append(Q(seasons__season=season))
                msg.append('Season={}'.format(season))
            if masspart:
                queries.append(Q(mass_parts__part=masspart))
                msg.append('Masspart={}'.format(masspart))
            if voicing:
                queries.append(Q(voicing__voicing=voicing))
                msg.append('Vvoicing={}'.format(voicing))
            if language:
                queries.append(Q(language__language=language))
                msg.append('Language={}'.format(language))

            if combinator == 'OR':
                query = reduce(operator.or_, queries)
                query_str = " OR ".join(msg)
            else:
                query = reduce(operator.and_, queries)
                query_str = " AND ".join(msg)



            # combine queries
            if combinator == 'OR':
                try:
                    query = reduce(operator.or_, queries)
                    query_str = " OR ".join(msg)
                except TypeError:
                    query = []
                    query_str = ""
            else:
                try:
                    query = reduce(operator.and_, queries)
                    query_str = " AND ".join(msg)
                except TypeError:
                    query = []
                    query_str = ""

            # execute query
            if not query:
                songs = Song.published_set.all()
            else:
                songs = Song.objects.filter(query)

            context = {}
            context['query_str'] = query_str
            context['songs'] = songs
            context['form'] = SongFilterForm()

            return render(request, template, context)
    else:
        form = SongFilterForm()
        return render(request, template, {'form' : form})

def reader_view(request, pk, slug):
    pass
    # song = get_object_or_404(Song, pk=pk, slug=slug)
    # response = HttpResponse(content_type="application/pdf")
    # response["Content-Disposition"] = "attachment; filename={}.pdf".format(song.slug)

    # canv = canvas.Canvas(response)

    # canv.drawString(100, 100, song.title)

    # canv.showPage()
    # canv.save()
    # return response

def filter_season(request, season):
    template = "song/filter_season.html"
    songs = Song.published_set.filter(seasons__season=season)
    paginator = Paginator(songs, 20)

    page = request.GET.get('page')
    songs = paginator.get_page(page)

    context = {}
    context['songs'] = songs
    context['season'] = season
    # context['is_paginated'] = True
    return render(request, template, context)

def filter_masspart(request, masspart):
    template = "song/filter_masspart.html"
    songs = Song.published_set.filter(mass_parts__part=masspart)
    paginator = Paginator(songs, 20)

    page = request.GET.get('page')
    songs = paginator.get_page(page)

    context = {}
    context['songs'] = songs
    context['masspart'] = masspart
    # context['is_paginated'] = True
    return render(request, template, context)

def filter_author(request, pk, slug):
    template = "song/filter_author.html"
    songs = Song.published_set.filter(authors__pk=pk, authors__slug=slug)
    paginator = Paginator(songs, 20)

    page = request.GET.get('page')
    songs = paginator.get_page(page)

    context = {}
    context['songs'] = songs
    context['author'] = Author.objects.get(pk=pk, slug=slug)
    # context['is_paginated'] = True
    return render(request, template, context)


