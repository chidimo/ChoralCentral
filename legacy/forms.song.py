"""Forms"""

from django import forms
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from django_addanother.widgets import AddAnotherWidgetWrapper

from .models import Voicing, Language, Season, MassPart, Song

OCASSIONS = ["sacred", "liturgical", "secular", "na"]
GENRES = [
    "anthem", "carol", "chorus", "folk music", "gregorian chant", "hymn", "litany", "madrigral", 
    "march", "mass", "motet", "popular music", "psalm", "requiem", "sequence", "na"]

GENRE_CHOICES = [(each, each.title()) for each in GENRES]
GENRE_CHOICES.insert(0, ("", "Select genre"))
OCASSION_CHOICES = [(each, each.title()) for each in OCASSIONS]

class SongLikeForm(forms.Form):
    pass

class NewVoicingForm(forms.ModelForm):
    class Meta:
        model = Voicing
        fields = ("name", )

        widgets = {
            "name" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Voicing"})
        }

    def clean(self):
        name = self.cleaned_data["name"].lower()
        if Voicing.objects.filter(name=name).exists():
            self.add_error("name", _("{} already exists".format(name)))

class EditVoicingForm(forms.ModelForm):
    class Meta:
        model = Voicing
        fields = ("name", )

class NewLanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ("name", )

        widgets = {
            "name" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Language"})
        }

    def clean(self):
        name = self.cleaned_data["name"].lower()
        if Language.objects.filter(name=name):
            self.add_error("name", _("{} already exists".format(name)))

class EditLanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ("name",)

class SongShareForm(forms.Form):
    receiving_email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : "Enter email address of the receiver."}),
    )
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : "Enter your name (optional)"})
    )

class SongFilterForm(forms.Form):
    combinator = forms.ChoiceField(
        choices = (
            ('or', 'OR'),
            ('and', 'AND')
        ),
        required=False,
        initial="and",
        widget=forms.Select(attrs={"class" : "form-control"}))

    genre = forms.ChoiceField(
        choices = GENRE_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class" : "form-control"}))

    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class" : "form-control",}))

    masspart = forms.ModelChoiceField(
        queryset=MassPart.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class" : "form-control",}))

    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class" : "form-control",}))

class NewSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["publish", "title", "ocassion", "genre", "year", "lyrics",
            "scripture_reference", "language", "tempo", "bpm",
            "divisions", "voicing", "authors", "seasons", "mass_parts",]

        widgets = {
            "title" : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : "Song title (100 characters max)"}),
            "genre" : forms.Select(choices=GENRE_CHOICES, attrs={'class' : 'form-control'}),
            "ocassion" : forms.Select(choices=OCASSION_CHOICES, attrs={'class' : 'form-control'}),
            "year" : forms.DateInput(
                attrs={'class' : 'form-control', 'placeholder' : "Composition year in <YYYY> format (Optional)"}),
            "lyrics" : forms.Textarea(
                attrs={'rows' : 5, 'columns' : 10, 'class' : 'form-control', 'placeholder' : "Optional. Supports markdown syntax"}),
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
                reverse_lazy('song:new_voicing')
                ),
            "language" : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('song:new_language'))}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].initial = Language.objects.get(name='english')
        self.fields['voicing'].initial = Voicing.objects.get(name='satb')
        self.fields['ocassion'].initial = "na"
        self.fields['genre'].initial = "na"
        self.fields['year'].initial = "1685"
        self.fields['tempo'].initial = 100
        self.fields['bpm'].initial = 4
        self.fields['divisions'].initial = 4
        self.fields['seasons'].initial = Season.objects.get(name='na')
        self.fields['mass_parts'].initial = MassPart.objects.get(name='na')

    def clean_title(self):
        """Make all titles lowercase"""
        return self.cleaned_data['title'].lower().strip()

class SongEditForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["publish", "title",  "ocassion", "genre", "year", "lyrics",
            "scripture_reference", "language", "tempo", "bpm",
            "divisions", "voicing", "authors", "seasons", "mass_parts",]

        widgets = {
            "title" : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : "Song title"}),
            "genre" : forms.Select(choices=GENRE_CHOICES ,attrs={'class' : 'form-control'}),
            "ocassion" : forms.Select(choices=OCASSION_CHOICES ,attrs={'class' : 'form-control'}),
            "year" : forms.DateInput(
                attrs={'class' : 'form-control', 'placeholder' : "Composition year in <YYYY> format (Optional)"}),
            "lyrics" : forms.Textarea(
                attrs={'rows' : 5, 'columns' : 10, 'class' : 'form-control', 'placeholder' : "Lyrics (optional). Supports markdown syntax"}),
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
                reverse_lazy('song:new_voicing')
                ),
            "language" : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('song:new_language'))}
