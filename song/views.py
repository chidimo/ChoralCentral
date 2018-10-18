"""Views"""

import json
import operator
from functools import reduce

from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as VAE
from django.views.decorators.cache import cache_page, cache_control
from django.utils.decorators import method_decorator

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin
from algoliasearch_django import get_adapter
import rules

from .utils import render_to_pdf, star_or_unstar_object

from siteuser.models import SiteUser
from redirect301.models import Url301

from .predicates import CONTEXT_MESSAGES

from .models import Song, Language, Voicing, Season, MassPart
from .forms import (SongLikeForm,
    NewVoicingForm, EditVoicingForm, NewLanguageForm,
    SongShareForm, NewSongForm, SongEditForm, SongFilterForm
)

class NewVoicing(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    form_class = NewVoicingForm
    template_name = "song/voicing_new.html"

class VoicingEdit(LoginRequiredMixin, generic.UpdateView):
    form_class = EditVoicingForm
    template_name = 'song/voicing_edit.html'

class LanguageIndex(generic.ListView):
    template_name = "song/language_index.html"
    context_object_name = 'languages'
    model = Language

class NewLanguage(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    form_class = NewLanguageForm
    template_name = 'song/language_new.html'

class LanguageEdit(LoginRequiredMixin, generic.CreateView):
    model = Language
    form_class = NewLanguageForm
    template_name = 'song/language_new.html'

class LanguageDetail(generic.DetailView):
    model = Language
    context_object_name = 'language'
    template_name = 'song/language_detail.html'

class LanguageDelete(generic.DeleteView):
    model = Language
    success_url = reverse_lazy('song:language_index')
    template_name = "confirm_delete.html"

class InstantSong(PaginationMixin, generic.ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'song/instant_song.html'
    # paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appId'] = settings.ALGOLIA['APPLICATION_ID']
        context['apiKey'] = settings.ALGOLIA['SEARCH_API_KEY']
        context['indexName'] = get_adapter(Song).index_name
        return context

def auto_song(request):
    context = {}
    context['appID'] = settings.ALGOLIA['APPLICATION_ID']
    context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
    context['indexName'] = get_adapter(Song).index_name
    return render(request, 'song/autocomplete_song.html', context)

def apply_song_filter(request):
    combinator = request.GET.get('combinator')
    genre = request.GET.get('genre')
    season_pk = request.GET.get('season')
    masspart_pk = request.GET.get('masspart')
    language_pk = request.GET.get('language')

    if all([(genre == ''), (season_pk == ''), (masspart_pk == ''), (language_pk == '')]):
        songs = Song.objects.filter(publish=True).select_related('voicing', 'language', 'creator').prefetch_related('seasons', 'mass_parts', 'authors')
        message = 'You did not make any selection.'
    else:
        queries = []
        message = []

        if genre:
            queries.append(Q(genre=genre))
            message.append("Genre '{}'".format(genre))
        try:
            queries.append(Q(seasons__id__exact=int(season_pk)))
            message.append(
                "Season '{}'".format(Season.objects.get(pk=season_pk).__str__())
            )
        except ValueError:
            pass
        try:
            queries.append(Q(mass_parts__id__exact=int(masspart_pk)))
            message.append(
                "Masspart '{}'".format(MassPart.objects.get(pk=masspart_pk).__str__())
            )
        except ValueError:
            pass
        try:
            queries.append(Q(language__id__exact=int(language_pk)))
            message.append(
                "Language '{}'".format(Language.objects.get(pk=language_pk).__str__())
            )
        except ValueError:
            pass

        if combinator == 'or':
            query = reduce(operator.or_, queries)
            query_str = " OR ".join(message)
        else:
            query = reduce(operator.and_, queries)
            query_str = " AND ".join(message)

        query = operator.and_(query, Q(publish=True)) # filter out unpublished songs and remove duplicates
        songs = Song.objects.filter(query).select_related('voicing', 'language', 'creator').prefetch_related('seasons', 'mass_parts', 'authors').distinct()
        message = "found {} results for {}".format(songs.count(), query_str)

    return {'success' : True, 'message' : message, 'songs' : songs}

def song_index(request):
    template = 'song/index.html'
    context = {}
    context['filter_form'] = SongFilterForm()

    # Handle stars via ajax
    if request.method == 'POST':
        if request.is_ajax():
            pk  = int(request.POST.get('pk')) # each song has unique pk
            model = 'song'
            app_label = 'song'
            siteuser = request.user.siteuser
            data = star_or_unstar_object(siteuser, pk, app_label, model)
            return JsonResponse(data)

    # if request.method == 'GET':
    #     if request.is_ajax():
    #         data = apply_song_filter(request)
    #         print("DATA\n", data)
    #         return JsonResponse(data)
    else:
        songs = Song.objects.select_related('voicing', 'language', 'creator').prefetch_related('seasons', 'mass_parts', 'authors').filter(publish=True)
        context['songs'] = songs
        return render(request, template, context)

# # @method_decorator(cache_control(must_revalidate=True, max_age=60*1), name='dispatch')
class SongIndex(PaginationMixin, generic.ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'song/index.html'
    paginate_by = 20

    # Handle stars via ajax
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            pk  = int(request.POST.get('pk')) # need to send this since I have multiple like buttons on this page
            model = 'song'
            app_label = 'song'
            siteuser = request.user.siteuser
            data = star_or_unstar_object(siteuser, pk, app_label, model)
            return JsonResponse(data)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filter_form'] = SongFilterForm()
        return context

    def get_queryset(self):
        return Song.objects.\
        select_related('voicing', 'language', 'creator').\
        prefetch_related('seasons', 'mass_parts', 'authors').filter(publish=True)

def song_redirect_301_view(request, pk, slug):
    template = '301.html'
    context = {}
    context['object'] = Song.objects.select_related('voicing', 'language', 'creator').get(pk=pk, slug=slug)
    return render(request, template, context)

def song_detail_view(request, pk, slug):
    template = 'song/detail.html'
    context = {}
    context['share_form'] = SongShareForm()

    # Handle stars via ajax
    if request.method == 'POST':
        if request.is_ajax():
            pk  = int(request.POST.get('pk')) # need to send this since I have multiple like buttons on this page
            model = request.POST.get('model')
            app_label = request.POST.get('app_label')
            siteuser = request.user.siteuser
            data = star_or_unstar_object(siteuser, pk, app_label, model)
            return JsonResponse(data)

    try:
        song = Song.objects.select_related('voicing', 'language', 'creator').get(pk=pk, slug=slug)
        context['song'] = song
        return render(request, template, context)
    except Song.DoesNotExist:
        # the url pointed to may have itself moved. So we work in a loop till we possibly find a match
        old_ref = slug
        while True:
            # There's a match in the url mapping table. Now we have to check if the song pointed to still exists
            try:
                ref = Url301.objects.get(app_name="song", old_reference=old_ref).new_reference
                try:
                    Song.objects.select_related('voicing', 'language', 'creator').get(pk=pk, slug=ref)
                    return redirect(reverse('song:song_moved', kwargs={'pk' : pk, 'slug' : ref}))
                except Song.DoesNotExist:
                    old_ref = ref
            # there is no match in the url mapping table. We're done
            except Url301.DoesNotExist:
                raise(Song.DoesNotExist)

def check_song_exists(request):
    title = request.GET.get('title', None).lower().strip()
    data = {'exists': Song.objects.filter(publish=True).filter(title=title).exists()}
    if data['exists']:
        data['song_url'] = Song.objects.get(title=title).get_absolute_url()
    return JsonResponse(data)

class NewSong(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    template_name = 'song/new.html'
    form_class = NewSongForm

    def form_valid(self, form):
        siteuser = self.request.user.siteuser
        form.instance.creator = siteuser
        if form.instance.genre == "gregorian chant":
            form.instance.bpm = None
            form.instance.divisions = None
        self.object = form.save()

        self.object.likes.add(siteuser)
        self.object.like_count = self.object.likes.count()
        self.object.save(update_fields=['like_count'])

        messages.success(self.request, "Song was successfully added")
        return redirect(self.get_success_url())

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['new_language_form'] = NewLanguageForm(auto_id="language_%s")
    #     return context

class SongEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Song
    form_class = SongEditForm
    template_name = 'song/edit.html'
    success_message = "Song updated successfully"

    def get_success_url(self):
        return reverse('siteuser:library', kwargs={'pk' : self.request.user.siteuser.pk, 'slug' : self.request.user.siteuser.slug})

    def get(self, request, *args, **kwargs):
        self.object = Song.objects.get(pk=self.kwargs["pk"])
        if rules.test_rule('edit_song', self.request.user, self.object):
            return self.render_to_response(self.get_context_data())
        messages.error(self.request, CONTEXT_MESSAGES['OPERATION_FAILED'])
        return redirect(self.get_success_url())

    def form_valid(self, form):
        old_ref = Song.objects.get(pk=self.kwargs["pk"]).slug

        if form.instance.genre == "gregorian chant":
            form.instance.bpm = None
            form.instance.divisions = None
        self.object = form.save()

        new_ref = self.object.slug

        # map the old refrence to a new one
        if old_ref != new_ref:
            Url301.objects.create(app_name="song", old_reference=old_ref, new_reference=new_ref)

        messages.success(self.request, "Song was successfully updated")
        return redirect(self.get_success_url())

def publish_song_shortcut(request, pk):
    song = Song.objects.get(pk=pk)
    if song.publish:
        song.publish = False
        song.save(update_fields=['publish'])
    else:
        song.publish=True
        song.save(update_fields=['publish'])
    return redirect(reverse('siteuser:library', kwargs={'pk' : request.user.siteuser.pk, 'slug' : request.user.siteuser.slug}))

class SongDelete(generic.DeleteView):
    model = Song
    template_name = "song/song_delete.html"

    def get_success_url(self):
        return reverse('siteuser:library', kwargs={'pk' : self.request.user.siteuser.pk, 'slug' : self.request.user.siteuser.slug})

    def get(self, request, *args, **kwargs):
        self.object = Song.objects.get(pk=self.kwargs["pk"])
        if rules.test_rule('edit_song', self.request.user, self.object):
            return self.render_to_response(self.get_context_data())
        messages.error(self.request, CONTEXT_MESSAGES['OPERATION_FAILED'])
        return redirect(self.get_success_url())

def reader_view(request, pk, slug):
    template = 'song/reader_view.html'
    song = Song.objects.get(pk=pk, slug=slug)
    context = {}
    context['song'] = song
    try:
        return render_to_pdf(request, template, context)
    except NameError:
        print("Windows system")
        return render(request, template, context)

def share_song_by_mail(request, pk, slug):
    context = {}
    from_email = settings.EMAIL_HOST_USER

    if request.method == 'GET':
        song = Song.objects.get(pk=pk, slug=slug)

        subject = 'Song share from ChoralCentral'
        context['song'] = song
        context['song_link'] = request.build_absolute_uri(song.get_absolute_url())

        form = SongShareForm(request.GET)
        if form.is_valid():
            form = form.cleaned_data
            receiving_email = form['receiving_email'].strip()
            name = form['name']
            context['name'] = name

            text_email = render_to_string("song/share_song_by_mail.txt", context)
            html_email = render_to_string("song/share_song_by_mail.html", context)
            msg = EmailMultiAlternatives(subject, text_email, from_email, [receiving_email])
            msg.attach_alternative(html_email, "text/html")
            msg.send()
            messages.success(request, "Song was successfully sent to {}".format(receiving_email))
            return redirect(song.get_absolute_url())

        else:
            messages.error(request, "Invalid email.")
            return redirect(song.get_absolute_url()) 
