
"""Views"""
import operator
from functools import reduce

import json
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, render, redirect
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

from universal.utils import render_to_pdf

from author.models import Author
from siteuser.models import SiteUser

from .models import Voicing, Language, Season, MassPart, Song
from .forms import (
    NewVoicingForm, EditVoicingForm,
    NewLanguageForm, EditLanguageForm,
    ShareForm, NewSongForm, SongEditForm, SongFilterForm
)

class NewVoicing(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    form_class = NewVoicingForm
    template_name = "song/voicing_new.html"

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)
        return super(NewVoicing, self).form_valid(form)

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

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)
        return super(NewLanguage, self).form_valid(form)

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

@login_required
@require_POST
def song_like_view(request):
    if request.method == 'POST':
        user = SiteUser.objects.get(user=request.user)
        pk = request.POST.get('pk', None)
        song = get_object_or_404(Song, pk=pk)

        if song.likes.filter(pk=user.pk).exists():
            song.likes.remove(user)
            song.like_count = song.likes.count()
            song.save(update_fields=['like_count'])
            message = "You unstarred this song.\n {} now has {} stars".format(song.title, song.like_count)
        else:
            song.likes.add(user)
            song.like_count = song.likes.count()
            song.save(update_fields=['like_count'])
            message = "You starred this song.\n {} now has {} stars".format(song.title, song.like_count)
    context = {'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

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
        return Song.objects.filter(publish=True)

class SongDetail(generic.DetailView):
    model = Song
    context_object_name = 'song'
    template_name = 'song/detail.html'

    def get_context_data(self, **kwargs):
        context = super(SongDetail, self).get_context_data(**kwargs)
        context['share_form'] = ShareForm()
        return context
    # add view counter here

class NewSong(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    template_name = 'song/new.html'
    form_class = NewSongForm

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)

        if (form.instance.first_line == "") and (form.instance.lyrics != ""):
            form.instance.first_line = form.instance.lyrics.split("\n")[0]
        self.object = form.save()
        self.object.likes.add(SiteUser.objects.get(user=self.request.user))

        self.object.like_count = self.object.likes.count()
        self.object.save(update_fields=['like_count'])
        messages.success(self.request, "Song was successfully added")
        return redirect(self.get_success_url())

class SongEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Song
    form_class = SongEditForm
    template_name = 'song/edit.html'
    success_message = "Song updated successfully"

class SongDelete(generic.DeleteView):
    model = Song
    template_name = "song/song_delete.html"

    def get_success_url(self):
        return reverse_lazy('siteuser:detail', kwargs={'pk' : self.request.user.siteuser.pk, 'slug' : self.request.user.siteuser.slug})

class FilterSongs(PaginationMixin, SuccessMessageMixin, generic.ListView):
    model = Song
    template_name = "song/index.html"
    context_object_name = "songs"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(FilterSongs, self).get_context_data(**kwargs)
        context['form'] = SongFilterForm()
        return context

    def _build_query(self, **kwargs):
        queries = []
        msg = []

        for key, value in kwargs.items():
            if key == "combinator":
                continue
            if value == None:
                continue
            query_string = ("('{}__id__exact', {})".format(key, value.id))
            messages.success(self.request, "query_string {}".format(query_string))
            queries.append(query_string)
            msg.append('{}={}'.format(key, value))

        if kwargs.get("combinator") == 'OR':
            # if query = []
            try:
                query = reduce(operator.or_, queries)
                query_msg = " OR ".join(msg)
            except TypeError:
                query = []
                query_msg = ""
        else:
            try:
                query = reduce(operator.and_, queries)
                query_msg = " AND ".join(msg)
            except TypeError:
                query = []
                query_msg = ""
        return query, query_msg

    def get_queryset(self):
        if self.request.method == 'GET':
            form = SongFilterForm(self.request.GET)

            if form.is_valid():
                data = form.cleaned_data
                combinator = data['combinator']
                season = data['season']
                masspart = data['masspart']
                voicing = data["voicing"]
                language = data["language"]
                author = data['author']

                query, msg = self._build_query(
                    authors=author, seasons=season, mass_parts=masspart,
                    voicing=voicing, language=language, combinator=combinator)

                if query:
                    messages.success(self.request, "Search msg {}".format(msg))
                    messages.success(self.request, "Search query {}".format(query))
                    return Song.objects.filter(query)
                else:
                    messages.success(self.request, "You did not make any selection.")
                    return Song.objects.filter(publish=True)

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

        form = ShareForm(request.GET)
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

def share_on_facebook(request, pk, slug):
    pass

