"""Various forms for admin page"""

from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper

from siteuser.models import SiteUser
from song.models import Song

from .models import Request, Reply

class NewRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ("title", )

        widgets = {
            "title" : forms.TextInput(
                attrs={"class" : "form-control", "placeholder" : "Name of song you wish to get"})
        }

    def clean(self):
        title = self.cleaned_data.get("title", None)
        if Request.objects.filter(title=title.lower()):
            msg = _("{} already exists".format(title))
            self.add_error('title', msg)

class RequestEditForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ("title", "status")

        widgets = {
            "title" : forms.TextInput(attrs={"class" : "form-control"}),
            "status" : forms.Select(attrs={"class" : "form-control"})
        }

class ReplyCreateFromRequestForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ("request", "song")

        widgets = {
            "request" : forms.Select(attrs={"class" : "form-control"}),
            "song" : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('song:new'))
        }

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop("pk")
        user = kwargs.pop("user")
        super(ReplyCreateFromRequestForm, self).__init__(*args, **kwargs)
        if pk:
            self.fields["request"].queryset = Request.objects.filter(pk=pk)
            self.fields["request"].initial = Request.objects.get(pk=pk)
        if user:
            f = Q(creator__user=user) & Q(publish=True)
            self.fields["song"].queryset = Song.objects.filter(f)

    def clean(self):
        song = self.cleaned_data["song"]
        if Reply.objects.filter(song=song).exists():
            msg = _("This song is already listed as a reply to {}".format(song.reply.request))
            self.add_error('song', msg)
