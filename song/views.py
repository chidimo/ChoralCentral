
"""Views"""

import os
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

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin
from algoliasearch_django import get_adapter

from siteuser.models import SiteUser
from .models import Song
from masspart.models import MassPart
from season.models import Season
from language.models import Language
from voicing.models import Voicing

from .forms import NewSongForm, SongEditForm, SongFilterForm

# pylint: disable=R0901, C0111

def instant_song(request):
    context = {}
    context['appID'] = settings.ALGOLIA['APPLICATION_ID']
    context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
    context['indexName'] = get_adapter(Song).index_name
    context['song_list'] = Song.published_set.all()
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
    context_object_name = 'song_list'
    template_name = 'song/song_index.html'
    paginate_by = 15

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

class NewSong(LoginRequiredMixin, generic.CreateView):
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

class FilterSongs(generic.ListView):
    context_object_name = "filtered"
    template_name = "song/filter_result.html"

    def get_queryset(self):
        form = SongFilterForm(self.request.GET)
        if form.is_valid():
            form = form.cleaned_data
        pass # finish later

def filter_songs(request):
    if "season" in request.GET:
        form = SongFilterForm(request.GET)
        template = "song/filter_result.html"
        if form.is_valid():
            form = form.cleaned_data
            print(form)
            season = form['season']
            mass_part = form['mass_part']
            voicing = form["voicing"]
            language = form["language"]

            filtered = Song.published_set.all()

            if season == "":
                pass
            else:
                seas = Season.objects.get(season=season)
                filtered = filtered.filter(seasons=seas)

            if mass_part == "":
                pass
            else:
                mps = MassPart.objects.get(part=mass_part)
                filtered = filtered.filter(mass_parts=mps)

            if voicing == "":
                pass
            else:
                voi = Voicing.objects.get(voicing=voicing)
                filtered = filtered.filter(voicing=voi)

            if language == "":
                pass
            else:
                lan = Language.objects.get(language=language)
                filtered = filtered.filter(language=lan)

            form = SongFilterForm()
            total_found = filtered.count()

            try:
                page = request.GET.get("page", 1)
            except PageNotAnInteger:
                page = 1

            p = Paginator(filtered, request=request, per_page=10)
            songs = p.page(page)

            context = {'filtered' : songs, "total_found" : total_found, 'form' : form}
            return render_to_response(template, context)
    else:
        form = SongFilterForm()
        template = "song/filter_result.html"
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
