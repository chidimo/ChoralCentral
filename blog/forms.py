"""Blog Forms"""

from django import forms
from siteuser.models import SiteUser
from song.models import Song
from .models import Post, Comment

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("publish", "title", "song", "subtitle", "body")

        widgets = {
                   "song" : forms.Select(attrs={'class' : 'form-control'}),
                   "title" : forms.TextInput(
                       attrs={'class' : 'form-control', "placeholder" : "Title"}),

                    "subtitle" : forms.TextInput(
                       attrs={'class' : 'form-control', "placeholder" : "Subtitle (optional)"}),

                    "body" : forms.Textarea(
                       attrs={'class' : 'form-control', "placeholder" : "Body"}),
                  }

    def __init__(self, *args, **kwargs):
        """How to do query in forms"""
        user = kwargs.pop("user")
        super(NewPostForm, self).__init__(*args, **kwargs)
        originator = SiteUser.objects.get(user=user)
        self.fields['song'].queryset = Song.objects.filter(originator=originator)

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("publish", "title", "subtitle", "song", "body", )

        widgets = {
                   "song" : forms.Select(attrs={'class' : 'form-control'}),
                   "title" : forms.TextInput(
                       attrs={'class' : 'form-control', "placeholder" : "Title"}),
                    "subtitle" : forms.TextInput(
                       attrs={'class' : 'form-control', "placeholder" : "Subtitle (optional)"}),
                   "body" : forms.Textarea(
                       attrs={'class' : 'form-control', "placeholder" : "Body"}),
                  }

class PostCreateFromSongForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "subtitle", "body")

        widgets = {"song" : forms.Select(attrs={'class' : 'form-control'}),
                   "title" : forms.TextInput(
                       attrs={'class' : 'form-control', "placeholder" : "Post title"}),
                    "subtitle" : forms.TextInput(
                       attrs={'class' : 'form-control', "placeholder" : "Subtitle (optional)"}),
                   "body" : forms.Textarea(
                       attrs={'class' : 'form-control', "placeholder" : "Body"}),
                  }

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment", )

        widgets = {
            "comment" : forms.Textarea(
                attrs={'class' : 'form-control', "placeholder" : "Type your comments."})
        }

class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment", )

        widgets = {
            "comment" : forms.Textarea(
                attrs={'class' : 'form-control', "placeholder" : "Type your comments."})
        }

class CommentNumberForm(forms.Form):
    number = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class' : 'form-control', 'placeholder' : "Number of comments to display"}))

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(
        attrs={'class' : 'form-control', 'placeholder' : "Search posts."}
    ))
