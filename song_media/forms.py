"""forms"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Sheet, Midi, VideoLink

from siteuser.models import SiteUser
from song.models import Song

class NewSheetForm(forms.ModelForm):
    class Meta:
        model = Sheet
        fields = ("song", "notation", "file", "part")

        widgets = {"song" : forms.Select(attrs={'class' : 'form-control'}),
                   "part" : forms.Select(attrs={'class' : 'form-control'}),
                   "notation" : forms.Select(attrs={'class' : 'form-control'}),
                #    "file" : forms.ClearableFileInput(),
                  }

    def __init__(self, *args, **kwargs):
        """How to do query in forms"""
        user = kwargs.pop('user')
        pk = kwargs.pop('pk')

        super(NewSheetForm, self).__init__(*args, **kwargs)
        originator = SiteUser.objects.get(user=user)
        if pk:
            self.fields['song'].queryset = Song.objects.filter(pk=pk)
            self.fields['song'].initial = Song.objects.get(pk=pk)
        else:
            self.fields['song'].queryset = Song.objects.filter(originator=originator)

class NewMidiForm(forms.ModelForm):
    class Meta:
        model = Midi
        fields = ("song", "file", "part")

        widgets = {"song" : forms.Select(attrs={'class' : 'form-control'}),
                   "part" : forms.Select(attrs={'class' : 'form-control'}),
                #    "file" : forms.ClearableFileInput(),
                  }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        pk = kwargs.pop('pk')

        super(NewMidiForm, self).__init__(*args, **kwargs)
        originator = SiteUser.objects.get(user=user)
        if pk:
            self.fields['song'].queryset = Song.objects.filter(pk=pk)
            self.fields['song'].initial = Song.objects.get(pk=pk)
        else:
            self.fields['song'].queryset = Song.objects.filter(originator=originator)

class NewVideoLinkForm(forms.ModelForm):
    class Meta:
        model = VideoLink
        fields = ("song", "video_link",)

        widgets = {
            "song" : forms.Select(attrs={'class' : 'form-control'}),
            "video_link" : forms.URLInput(
                attrs={'class' : 'form-control', 'placeholder' : 'Video Url'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        pk = kwargs.pop('pk')

        super(NewVideoLinkForm, self).__init__(*args, **kwargs)
        originator = SiteUser.objects.get(user=user)
        if pk:
            self.fields['song'].queryset = Song.objects.filter(pk=pk)
            self.fields['song'].initial = Song.objects.get(pk=pk)
        else:
            self.fields['song'].queryset = Song.objects.filter(originator=originator)
