"""Forms"""

from django import forms
from django.forms.fields import DateField
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django_addanother.widgets import AddAnotherWidgetWrapper

from .models import Song
from season.models import Season
from masspart.models import MassPart
from voicing.models import Voicing
from language.models import Language

# pylint: disable=C0326, C0301, C0103, C0111

class GetEmailAddressForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : "Enter email"})
    )

class SongFilterForm(forms.Form):
    combinator = forms.ChoiceField(
        choices = (
            ('OR', 'OR'),
            ('AND', 'AND')
        ),
        required=True,
        initial = 'OR',
        widget=forms.Select(attrs={"class" : "form-control"}))

    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class" : "form-control",}))

    masspart = forms.ModelChoiceField(
        queryset=MassPart.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class" : "form-control",}))

    voicing = forms.ModelChoiceField(
        queryset=Voicing.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class" : "form-control",}))

    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class" : "form-control",}))

class NewSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["publish", "title", "compose_date",
                  "lyrics", "first_line", "scripture_reference", "language",
                  "tempo", "bpm", "divisions", "voicing",
                  "authors", "seasons", "mass_parts",]

        widgets = {
            "title" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Song title"}),
            "compose_date" : forms.DateInput(
                attrs={'class' : 'form-control', 'placeholder' : "Composition date YYYY-MM-DD (optional)"}),
            "lyrics" : forms.Textarea(
                attrs={'rows' : 5, 'columns' : 10, 'class' : 'form-control', 'placeholder' : "Lyrics (optional). Supports markdown syntax"}),
            "first_line" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "First line (optional)"}),
            "scripture_reference" : forms.TextInput(
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
        fields = ["publish", "title", "compose_date",
                  "lyrics", "first_line", "scripture_reference", "language",
                  "tempo", "bpm", "divisions", "voicing",
                  "authors", "seasons", "mass_parts",]

        widgets = {
            "title" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Song title"}),
            "compose_date" : forms.DateInput(
                attrs={'class' : 'form-control', 'placeholder' : "Composition date YYYY-MM-DD (optional)"}),
            "lyrics" : forms.Textarea(
                attrs={'rows' : 5, 'columns' : 10, 'class' : 'form-control', 'placeholder' : "Lyrics (optional). Supports markdown syntax"}),
            "first_line" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "First line (optional)"}),
            "scripture_reference" : forms.TextInput(
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
