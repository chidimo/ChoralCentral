"""Views"""

import operator
from functools import reduce

from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
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

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin
from algoliasearch_django import get_adapter
import rules

from .utils import render_to_pdf

from siteuser.models import SiteUser
from redirect301.models import Url301

from .predicates import CONTEXT_MESSAGES

from .models import Song, Language#, Voicing, Season, MassPart, Song
from .forms import (
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
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

@require_POST
@login_required
def song_like_view(request):
    if request.method == 'POST':
        siteuser = request.user.siteuser
        pk = request.POST.get('pk', None)
        song = Song.objects.get(pk=int(pk))

        if song.likes.filter(pk=siteuser.pk).exists():
            song.likes.remove(siteuser)
            msg = "You unstarred this song.\n"
        else:
            song.likes.add(siteuser)
            msg = "You starred this song.\n"
    song.like_count = song.likes.count()
    song.save(update_fields=['like_count'])
    context = {'msg' : msg, 'like_count' : song.like_count, 'title' : song.title}
    return JsonResponse(context)

class SongIndex(PaginationMixin, generic.ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'song/index.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(SongIndex, self).get_context_data(**kwargs)
        context['form'] = SongFilterForm()
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
            redirect_url = Url301.objects.create(app_name="song", old_reference=old_ref, new_reference=new_ref)

        messages.success(self.request, "Song was successfully updated")
        return redirect(self.get_success_url())

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

class FilterSongs(PaginationMixin, SuccessMessageMixin, generic.ListView):
    model = Song
    template_name = "song/index.html"
    context_object_name = "songs"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(FilterSongs, self).get_context_data(**kwargs)
        context['form'] = SongFilterForm()
        context['is_filter'] = "yes"
        return context

    def get_queryset(self):
        if self.request.method == 'GET':
            form = SongFilterForm(self.request.GET)
            if form.is_valid():
                form = form.cleaned_data
                combinator = form['combinator']
                genre = form['genre']
                season = form['season']
                masspart = form['masspart']
                language = form["language"]

                if (genre == '') and (season == None) and (masspart == None) and (language == None):
                    messages.success(self.request, "You did not make any selection.")
                    return Song.objects.select_related('voicing', 'language', 'creator').\
                    prefetch_related('seasons', 'mass_parts', 'authors').filter(publish=True)

                queries = []
                msg = []
                if genre:
                    queries.append(Q(genre=genre))
                    msg.append("Genre '{}'".format(genre))
                if season:
                    queries.append(Q(seasons__id__exact=season.id))
                    msg.append("Season '{}'".format(season))
                if masspart:
                    queries.append(Q(mass_parts__id__exact=masspart.id))
                    msg.append("Masspart '{}'".format(masspart))
                if language:
                    queries.append(Q(language__id__exact=language.id))
                    msg.append("Language '{}'".format(language))

                if combinator == 'or':
                    query = reduce(operator.or_, queries)
                    query_str = " OR ".join(msg)
                else:
                    query = reduce(operator.and_, queries)
                    query_str = " AND ".join(msg)

                query = operator.and_(query, Q(publish=True)) # filter out unpublished songs and remove duplicates
                results = Song.objects.filter(query).select_related('voicing', 'language', 'creator').\
                prefetch_related('seasons', 'mass_parts', 'authors').distinct()
                messages.success(self.request, "found {} results for {}".format(results.count(), query_str))
                return results

def reader_view(request, pk, slug):
    template = 'song/reader_view.html'
    song = Song.objects.get(pk=pk, slug=slug)
    context = {}
    context['song'] = song
    # return render(request, template, context)
    return render_to_pdf(request, template, context)

def share_song_by_mail(request, pk, slug):
    context = {}

    from_email = settings.EMAIL_HOST_USER

    if request.method == 'GET':
        song = Song.objects.get(pk=pk, slug=slug)

        subject = '{} was shared with you from ChoralCentral'.format(song.title)
        context['song'] = song
        context['song_link'] = request.build_absolute_uri(song.get_absolute_url())

        form = SongShareForm(request.GET)
        if form.is_valid():
            form = form.cleaned_data
            receiving_emails = form['receiving_emails']
            name = form['name']
            context['name'] = name

            email_list = [email.strip() for email in receiving_emails.split(',')]
            if len(email_list) > 3:
                messages.error(request, "Too many emails. Please enter at most 5 email addresses.")
                return redirect(song.get_absolute_url())
            good_emails = []
            bad_emails = []

            for email in email_list:
                try:
                    validate_email(email)
                    good_emails.append(email)
                except VAE:
                    bad_emails.append(email)

            if good_emails:
                for email in good_emails: # avoid mail address bundling in inbox.
                    text_email = render_to_string("song/share_song_by_mail.txt", context)
                    html_email = render_to_string("song/share_song_by_mail.html", context)
                    msg = EmailMultiAlternatives(subject, text_email, from_email, [email])
                    msg.attach_alternative(html_email, "text/html")
                    msg.send()
                success_msg = "Song was successfully sent to {}".format(", ".join(good_emails))
                messages.success(request, success_msg)
            if bad_emails:
                error_msg = "Song was not sent to the following invalid emails: {}".format(", ".join(bad_emails))
                messages.error(request, error_msg)

            return redirect(song.get_absolute_url())
