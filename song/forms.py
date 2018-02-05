"""Forms"""

from django import forms
from django.utils import timezone
from django.forms.fields import DateField
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django_addanother.widgets import AddAnotherWidgetWrapper

from siteuser.models import SiteUser
from .models import Song
from season.models import Season
from masspart.models import MassPart
from voicing.models import Voicing
from language.models import Language

# pylint: disable=C0326, C0301, C0103, C0111

class SongFilterForm(forms.Form):
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        # initial=0,
        required=False,
        widget=forms.Select(attrs={"class" : "form-control",}))

    masspart = forms.ModelChoiceField(
        queryset=MassPart.objects.all(),
        # initial=0,
        required=False,
        widget=forms.Select(attrs={"class" : "form-control",}))

    voicing = forms.ModelChoiceField(
        queryset=Voicing.objects.all(),
        # initial=0,
        required=False,
        widget=forms.Select(attrs={"class" : "form-control",}))

    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        # initial=0,
        required=False,
        widget=forms.Select(attrs={"class" : "form-control",}))

class NewSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["status", "title", "compose_date",
                  "lyrics", "first_line", "scripture_ref", "language",
                  "tempo", "bpm", "divisions", "voicing",
                  "authors", "seasons", "mass_parts",]

        widgets = {
            "status" : forms.Select(attrs={'class' : 'form-control'}),
            "title" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Song title"}),
            "compose_date" : forms.DateInput(
                attrs={'class' : 'form-control', 'placeholder' : "Composition date YYYY-MM-DD (optional)"}),
            "lyrics" : forms.Textarea(
                attrs={'rows' : 5, 'columns' : 10, 'class' : 'form-control', 'placeholder' : "Lyrics (optional). Markdown supported"}),
            "first_line" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "First line (optional)"}),
            "scripture_ref" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Scripture reference (optional)"}),
            "seasons" : forms.SelectMultiple(attrs={'class' : 'form-control'}),
            "mass_parts" : forms.SelectMultiple(attrs={'class' : 'form-control'}),
            "tempo" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : "Tempo (optional)"}),
            "bpm" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : "Beats per minute (optional)"}),
            "divisions" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : "Divisions (optional)"}),

            "authors" : AddAnotherWidgetWrapper(
                forms.SelectMultiple(attrs={'class' : 'form-control'}),
                reverse_lazy('author:new')
                ),
            "voicing" : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('voicing:new')
                ),
            "language" : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('language:new'))}

class SongEditForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["status", "title", "compose_date",
                  "lyrics", "first_line", "scripture_ref", "language",
                  "tempo", "bpm", "divisions", "voicing",
                  "authors", "seasons", "mass_parts",]

        widgets = {
            "status" : forms.Select(attrs={'class' : 'form-control'}),
            "title" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Song title"}),
            "compose_date" : forms.DateInput(
                attrs={'class' : 'form-control', 'placeholder' : "Composition date YYYY-MM-DD (optional)"}),
            "lyrics" : forms.Textarea(
                attrs={'rows' : 5, 'columns' : 10, 'class' : 'form-control', 'placeholder' : "Lyrics (optional). Markdown supported"}),
            "first_line" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "First line (optional)"}),
            "scripture_ref" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Scripture reference (optional)"}),
            "seasons" : forms.SelectMultiple(attrs={'class' : 'form-control'}),
            "mass_parts" : forms.SelectMultiple(attrs={'class' : 'form-control'}),
            "tempo" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : "Tempo (optional)"}),
            "bpm" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : "Beats per minute (optional)"}),
            "divisions" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : "Divisions (optional)"}),

            "authors" : AddAnotherWidgetWrapper(
                forms.SelectMultiple(attrs={'class' : 'form-control'}),
                reverse_lazy('author:new')
                ),
            "voicing" : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('voicing:new')
                ),
            "language" : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('language:new'))}
