"""Various forms for admin page"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Request, Reply
from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper

from siteuser.models import SiteUser
from song.models import Song

class RequestCreateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ("request", )

        widgets = {
            "request" : forms.TextInput(
                attrs={"class" : "form-control", "placeholder" : "Request"})
        }

    def clean_request(self):
        request = self.cleaned_data.get("request", None)
        if Request.objects.filter(request=request.upper()):
            raise forms.ValidationError(_("{} already exists".format(request)))
        return request

class RequestEditForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ("request", "status")

        widgets = {
            "request" : forms.TextInput(attrs={"class" : "form-control"}),
            "status" : forms.Select(attrs={"class" : "form-control", "placeholder" : "Status"})
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

    def clean_song(self):
        song = self.cleaned_data["song"]
        if Reply.objects.filter(song=song).exists():
            raise forms.ValidationError("This song has already been added to this request")
        return song

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop("pk")
        user = kwargs.pop("user")
        super(ReplyCreateFromRequestForm, self).__init__(*args, **kwargs)
        if pk:
            self.fields["request"].initial = Request.objects.get(pk=pk)
        if user:
            originator = SiteUser.objects.get(user=user)
            self.fields["song"].queryset = Song.objects.filter(originator=originator)
