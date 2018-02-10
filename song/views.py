
"""Views"""

import json
import pprint
# from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Sum
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import View, generic
from django.urls import reverse_lazy
from django.shortcuts import render, render_to_response, reverse, redirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, Page, EmptyPage

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin
from algoliasearch_django import get_adapter

from siteuser.models import SiteUser
from .models import Song

from .forms import NewSongForm, SongEditForm, SongFilterForm

# pylint: disable=R0901, C0111

def instant_song(request):
    context = {}
    context['appID'] = settings.ALGOLIA['APPLICATION_ID']
    context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
    context['indexName'] = get_adapter(Song).index_name

    # songs = Song.published_set.all()
    # context['songs'] = songs
    # paginator = Paginator(songs, 1)
    # page = request.GET.get('page')
    # songs = paginator.get_page(page)

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
            message = "You unstarred this song"
        else:
            song.likes.add(user)
            message = "You starred this song"
    context = {'likes_count' : song.song_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

class SongIndex(PaginationMixin, generic.ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'song/index.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        print("IP Address for debug-toolbar: " + self.request.META['REMOTE_ADDR'])
        context = super(SongIndex, self).get_context_data(**kwargs)
        context['appID'] = settings.ALGOLIA['APPLICATION_ID']
        context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
        context['indexName'] = get_adapter(Song).index_name
        context["song_count"] = Song.published_set.count()
        context['form'] = SongFilterForm()
        return context

    def get_queryset(self):
        return Song.published_set.all().annotate(Count("likes")).order_by("-likes__count")

class SongDetail(generic.DetailView):
    model = Song
    context_object_name = 'song'
    template_name = 'song/detail.html'

class SongReader(generic.DetailView):
    model = Song
    context_object_name = 'song'
    template_name = 'song/reader.html'

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
            season = form['season']
            masspart = form['masspart']
            voicing = form["voicing"]
            language = form["language"]

            if season:
                songs = Song.published_set.filter(seasons__season=season)
            if masspart:
                songs = Song.published_set.filter(mass_parts__part=masspart)
            if voicing:
                songs = Song.published_set.filter(voicing__voicing=voicing)
            if language:
                songs = Song.published_set.filter(language__language=language)

            paginator = Paginator(songs, 10)
            page = request.GET.get('page')
            songs = paginator.get_page(page)

            form = SongFilterForm()
            context = {}
            context['found'] = songs.count()
            context['songs'] = songs
            context['is_paginated'] = True
            context['form'] = form

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
    paginator = Paginator(songs, 10)

    page = request.GET.get('page')
    songs = paginator.get_page(page)

    context = {}
    context['songs'] = songs
    # context['is_paginated'] = True

    return render(request, template, context)

def filter_masspart(request, masspart):
    template = "song/filter_masspart.html"
    songs = Song.published_set.filter(mass_parts__part=masspart)
    paginator = Paginator(songs, 10)

    page = request.GET.get('page')
    songs = paginator.get_page(page)

    context = {}
    context['songs'] = songs
    # context['is_paginated'] = True

    return render(request, template, context)

def filter_author(request, pk, slug):
    template = "song/filter_author.html"
    songs = Song.published_set.filter(authors__pk=pk, authors__slug=slug)
    paginator = Paginator(songs, 10)

    page = request.GET.get('page')
    songs = paginator.get_page(page)

    context = {}
    context['songs'] = songs
    # context['is_paginated'] = True

    return render(request, template, context)


