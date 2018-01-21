"""forms"""

from django import forms
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from django_addanother.widgets import AddAnotherWidgetWrapper

from .models import VocalPart, ScoreNotation, Score, Midi, VideoLink

from siteuser.models import SiteUser
from song.models import Song

class NewVocalPartForm(forms.ModelForm):
    class Meta:
        model = VocalPart
        fields = ('name', )

        widgets = {
            'name' : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : 'Part name'})
                }

class NewScoreNotationForm(forms.ModelForm):
    class Meta:
        model = ScoreNotation
        fields = ('name', )

        widgets = {
            'name' : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : 'Notation name'})
                }

class NewScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ('song', 'notation', 'file', 'part')

        widgets = {'song' : forms.Select(attrs={'class' : 'form-control'}),

                   'part' : AddAnotherWidgetWrapper(
                       forms.SelectMultiple(attrs={'class' : 'form-control'}),
                       reverse_lazy('song-media:new_part')),

                   'notation' : AddAnotherWidgetWrapper(
                       forms.SelectMultiple(attrs={'class' : 'form-control'}),
                       reverse_lazy('song-media:new_notation')),
                  }

    def __init__(self, *args, **kwargs):
        """Query in forms"""
        user = kwargs.pop('user')
        pk = kwargs.pop('pk')

        super(NewScoreForm, self).__init__(*args, **kwargs)
        # originator = SiteUser.objects.get(user=user)
        if pk:
            self.fields['song'].queryset = Song.objects.filter(pk=pk)
            self.fields['song'].initial = Song.objects.get(pk=pk)
        else:
            self.fields['song'].queryset = Song.objects.filter(originator__user=user)
            # self.fields['song'].queryset = Song.objects.filter(originator=originator)

class NewMidiForm(forms.ModelForm):
    class Meta:
        model = Midi
        fields = ('song', 'file', 'part')

        widgets = {'song' : forms.Select(attrs={'class' : 'form-control'}),

                   'part' : AddAnotherWidgetWrapper(
                       forms.SelectMultiple(attrs={'class' : 'form-control'}),
                       reverse_lazy('song-media:new_part')),
                  }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        pk = kwargs.pop('pk')

        super(NewMidiForm, self).__init__(*args, **kwargs)
        # originator = SiteUser.objects.get(user=user)
        if pk:
            self.fields['song'].queryset = Song.objects.filter(pk=pk)
            self.fields['song'].initial = Song.objects.get(pk=pk)
        else:
            self.fields['song'].queryset = Song.objects.filter(originator__user=user)

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
        user = kwargs.pop('user')
        pk = kwargs.pop('pk')

        super(NewVideoLinkForm, self).__init__(*args, **kwargs)
        # originator = SiteUser.objects.get(user=user)
        if pk:
            self.fields['song'].queryset = Song.objects.filter(pk=pk)
            self.fields['song'].initial = Song.objects.get(pk=pk)
        else:
            self.fields['song'].queryset = Song.objects.filter(originator__user=user)
