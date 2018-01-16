"""Forms"""

from django import forms
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django_addanother.widgets import AddAnotherWidgetWrapper

from siteuser.models import SiteUser
from .models import Song
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

SEAS = [
    "ORDINARY TIME", "ADVENT", "CHRISTMAS", "LENT",
    "EASTER", "PENTECOST", "OTHER"
    ]
PARTS = [
    "ENTRANCE", "KYRIE", "GLORIA", "ACCLAMATION", "OFFERTORY",
    "COMMUNION", "SANCTUS", "AGNUS DEI", "RECESSION", "GENERAL","CAROL"
    ]

SEASON_CHOICES = [[each, each] for each in SEAS]
SEASON_CHOICES.insert(0, ("", "Select Season"))

MASS_CHOICES = [[each, each] for each in PARTS]
MASS_CHOICES.insert(0, ("", "Select Masspart"))

VOICING_CHOICES = [(each.voicing, each.voicing) for each in Voicing.objects.all()]
VOICING_CHOICES.insert(0, ("", "Select Voicing"))

LANGUAGE_CHOICES = [(each.language, each.language) for each in Language.objects.all()]
LANGUAGE_CHOICES.insert(0, ("", "Select Language"))

class SongFilterForm(forms.Form):
    # pass
    season = forms.ChoiceField(
        required=False, choices=SEASON_CHOICES, widget=forms.Select(
            attrs={'class':'form-control'}))
    mass_part = forms.ChoiceField(
        required=False, choices=MASS_CHOICES, widget=forms.Select(
            attrs={'class':'form-control'}))
    voicing = forms.ChoiceField(
        required=False, choices=VOICING_CHOICES, widget=forms.Select(
            attrs={'class':'form-control'}))
    language = forms.ChoiceField(
        required=False, choices=LANGUAGE_CHOICES, widget=forms.Select(
            attrs={'class':'form-control'}))

class SongCreateForm(forms.ModelForm):
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
