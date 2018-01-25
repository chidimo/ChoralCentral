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

TITLE = "Song title"
FIRST_LINE = "First line (optional)"
SCRIPTURE = "Scripture reference (optional)"
TEMPO = "Tempo (optional)"
BPM = "Beats per minute (optional)"
LYRICS = "Lyrics (optional)"
COMP_DATE = "Composition date YYYY-MM-DD (optional)"
DIVS = "Divisions (optional)"

LYRICS_HELP = """Markdown supported.
See basic markdown syntax [here](https://daringfireball.net/projects/markdown/basics)"""

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

        help_texts = {
            "lyrics" : LYRICS_HELP
        }

        widgets = {
            "status" : forms.Select(attrs={'class' : 'form-control'}),
            "title" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : TITLE}),
            "compose_date" : forms.DateInput(
                attrs={'class' : 'form-control', 'placeholder' : COMP_DATE}),
            "lyrics" : forms.Textarea(
                attrs={'rows' : 5, 'columns' : 10, 'class' : 'form-control', 'placeholder' : LYRICS}),
            "first_line" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : FIRST_LINE}),
            "scripture_ref" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : SCRIPTURE}),
            "seasons" : forms.SelectMultiple(attrs={'class' : 'form-control'}),
            "mass_parts" : forms.SelectMultiple(attrs={'class' : 'form-control'}),
            "tempo" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : TEMPO}),
            "bpm" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : BPM}),
            "divisions" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : DIVS}),

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
                attrs={'class' : 'form-control', 'placeholder' : TITLE}),
            "compose_date" : forms.DateInput(
                attrs={'class' : 'form-control', 'placeholder' : COMP_DATE}),
            "lyrics" : forms.Textarea(
                attrs={'rows' : 5, 'columns' : 10, 'class' : 'form-control', 'placeholder' : LYRICS}),
            "first_line" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : FIRST_LINE}),
            "scripture_ref" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : SCRIPTURE}),
            "seasons" : forms.SelectMultiple(attrs={'class' : 'form-control'}),
            "mass_parts" : forms.SelectMultiple(attrs={'class' : 'form-control'}),
            "tempo" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : TEMPO}),
            "bpm" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : BPM}),
            "divisions" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : DIVS}),

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
