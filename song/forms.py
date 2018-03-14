"""Forms"""

from django import forms
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django_addanother.widgets import AddAnotherWidgetWrapper

from .models import Voicing, Song
from season.models import Season
from masspart.models import MassPart
from voicing.models import Voicing
from language.models import Language
from author.models import Author

class NewVoicingForm(forms.ModelForm):
    class Meta:
        model = Voicing
        fields = ("voicing", )

        widgets = {
            "voicing" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Voicing"})
        }

    def clean_voicing(self):
        voicing = self.cleaned_data.get("voicing", None).upper()
        if Voicing.objects.filter(voicing=voicing).exists():
            raise forms.ValidationError(_("{} already exists".format(voicing)))
        return voicing

class EditVoicingForm(forms.ModelForm):
    class Meta:
        model = Voicing
        fields = ("voicing", )

class ShareForm(forms.Form):
    receiving_emails = forms.CharField(
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : "Enter any number of emails, separated by commas."}),
    )
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : "Enter your name (optional)"})
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

    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class" : "form-control",}))

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
            "publish" : forms.CheckboxInput(attrs={'class' : 'form-control'}),
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
