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
            raise forms.ValidationError(_("{} already exists".format(name)))
        return name

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
            raise forms.ValidationError(_("{} already exists".format(name)))
        return name

class NewScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ('song', 'notation', 'part', 'media_file')

        widgets = {'song' : forms.Select(attrs={'class' : 'form-control'}),

                   'part' : AddAnotherWidgetWrapper(
                       forms.Select(attrs={'class' : 'form-control'}),
                       reverse_lazy('song-media:new_part')),

                   'notation' : AddAnotherWidgetWrapper(
                       forms.Select(attrs={'class' : 'form-control'}),
                       reverse_lazy('song-media:new_notation')),

                    'media_file' : ClearableFileInput(attrs={'class' : 'form-control'}),
                  }

    def __init__(self, *args, **kwargs):
        """Query in forms"""
        pk = kwargs.pop('pk')
        super(NewScoreForm, self).__init__(*args, **kwargs)
        self.fields['song'].queryset = Song.objects.filter(pk=pk)
        self.fields['song'].initial = Song.objects.get(pk=pk)

    def clean(self):
        media_file = self.cleaned_data['media_file']
        fsize = media_file.size/1048576
        max_size = 5242880/1048576# limit size to 5MB
        if fsize > max_size:
            msg = "Attempting to upload {:.2f}MB file. Size must not exceed {:.2f}MB".format(fsize, max_size)
            self.add_error("media_file", msg)

class NewMidiForm(forms.ModelForm):
    class Meta:
        model = Midi
        fields = ('song', 'part', 'description', 'media_file')

        widgets = {'song' : forms.Select(attrs={'class' : 'form-control'}),

                   'part' : AddAnotherWidgetWrapper(
                       forms.Select(attrs={'class' : 'form-control'}),
                       reverse_lazy('song-media:new_part')),

                    'media_file' : ClearableFileInput(attrs={'class' : 'form-control'}),

                    'name' : forms.TextInput(
                        attrs={'class' : 'form-control', 'placeholder' : 'Notation name'}),

                    'description' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter a short description (optional)'}),
                  }

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')

        super(NewMidiForm, self).__init__(*args, **kwargs)
        self.fields['song'].queryset = Song.objects.filter(pk=pk)
        self.fields['song'].initial = Song.objects.get(pk=pk)

    def clean(self):
        media_file = self.cleaned_data['media_file']
        fsize = media_file.size/1048576
        max_size = 2097152/1048576 # limit size to 2MB
        if fsize > max_size:
            msg = "File is {:.2f}MB. Maximum allowed file size is {:.2f}MB".format(fsize, max_size)
            self.add_error("media_file", msg)

class NewVideoLinkForm(forms.ModelForm):
    class Meta:
        model = VideoLink
        fields = ('song', 'video_link',)

        widgets = {
            'song' : forms.Select(attrs={'class' : 'form-control'}),
            'video_link' : forms.URLInput(
                attrs={'class' : 'form-control', 'placeholder' : 'Video Url'})
        }

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        super(NewVideoLinkForm, self).__init__(*args, **kwargs)
        self.fields['song'].queryset = Song.objects.filter(pk=pk)
        self.fields['song'].initial = Song.objects.get(pk=pk)
