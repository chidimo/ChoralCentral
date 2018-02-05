"""Blog Forms"""

from django import forms
from siteuser.models import SiteUser
from song.models import Song
from .models import Post, Comment

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("status", "song", "title", "subtitle", "body")

        widgets = {"status" : forms.Select(attrs={'class' : 'form-control'}),
                   "song" : forms.Select(attrs={'class' : 'form-control'}),
                   "title" : forms.TextInput(
                       attrs={'class' : 'form-control', "placeholder" : "Post title"}),

                    "subtitle" : forms.TextInput(
                       attrs={'class' : 'form-control', "placeholder" : "Subtitle (optional)"}),

                    "body" : forms.Textarea(
                       attrs={'class' : 'form-control', "placeholder" : "Post body"}),
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
        fields = ("status", "song", "body", "title")

        widgets = {"status" : forms.Select(attrs={'class' : 'form-control'}),
                   "song" : forms.Select(attrs={'class' : 'form-control'}),
                   "title" : forms.TextInput(
                       attrs={'class' : 'form-control', "placeholder" : "Post title"}),
                   "body" : forms.Textarea(
                       attrs={'class' : 'form-control', "placeholder" : "Post body"}),
                  }

class PostCreateFromSongForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("body", "title")

        widgets = {"song" : forms.Select(attrs={'class' : 'form-control'}),
                   "title" : forms.TextInput(
                       attrs={'class' : 'form-control', "placeholder" : "Post title"}),
                   "body" : forms.Textarea(
                       attrs={'class' : 'form-control', "placeholder" : "Post body"}),
                  }

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment", )

        widgets = {
            "comment" : forms.Textarea(
                attrs={'rows' : 5, 'columns' : 20, 'class' : 'form-control', "placeholder" : "Add your thoughts here."})
        }

class CommentNumberForm(forms.Form):
    number = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class' : 'form-control', 'placeholder' : "Number of comments to display"}))

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(
        attrs={'class' : 'form-control', 'placeholder' : "Search posts."}
    ))
