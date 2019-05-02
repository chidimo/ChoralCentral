"""forms"""

from django import forms
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import ClearableFileInput

from django_addanother.widgets import AddAnotherWidgetWrapper

from .models import VocalPart, ScoreNotation, Score, Midi, VideoLink

from song.models import Song

class NewVocalPartForm(forms.ModelForm):
    class Meta:
        model = VocalPart
        fields = ('name', )

        widgets = {
            'name' : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : 'Part name'})
                }

    def clean_name(self):
        name = self.cleaned_data.get("name", None)
        if VocalPart.objects.filter(name=name).exists():
            raise forms.ValidationError(_(f"{name} already exists"))
        return name.lower()

class NewScoreNotationForm(forms.ModelForm):
    class Meta:
        model = ScoreNotation
        fields = ('name', )

        widgets = {
            'name' : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : 'Notation name'})
                }

    def clean_name(self):
        name = self.cleaned_data.get("name", None)
        if VocalPart.objects.filter(name=name).exists():
            raise forms.ValidationError(_(f"{name} already exists"))
        return name.lower()

class NewScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ('notation', 'part', 'media_file')

        widgets = {
            'part' : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('song-media:new_part')),
            'notation' : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('song-media:new_notation')),
            'media_file' : ClearableFileInput(attrs={'class' : 'form-control', 'accept' : '.pdf'}),
        }

    def clean(self):
        data = super().clean()
        media_file = data['media_file']
        fsize = media_file.size/(1024 * 1024)
        max_size = (1024 * 1024 * 5)/(1024 * 1024)# limit size to 5MB
        if fsize > max_size:
            msg = f"Attempting to upload {fsize}MB file. Size must not exceed {max_size:.2f}MB"
            self.add_error("media_file", msg)

class NewMidiForm(forms.ModelForm):
    class Meta:
        model = Midi
        fields = ('part', 'description', 'media_file')

        widgets = {
            'part' : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('song-media:new_part')),

            'media_file' : ClearableFileInput(attrs={'class' : 'form-control', 'accept' : '.mp3, .mid, .midi'}),

            'description' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter a short description (optional)'}),
        }

    def clean(self):
        media_file = self.cleaned_data['media_file']
        fsize = media_file.size/1048576
        max_size = 2097152/1048576 # limit size to 2MB
        if fsize > max_size:
            msg = f"File is {fsize}MB. Maximum allowed file size is {max_size}MB"
            self.add_error("media_file", msg)

class NewVideoLinkForm(forms.ModelForm):
    class Meta:
        model = VideoLink
        fields = ('video_link',)

        widgets = {
            'song' : forms.Select(attrs={'class' : 'form-control'}),
            'video_link' : forms.URLInput(
                attrs={'class' : 'form-control', 'placeholder' : 'Video Url'})
        }
