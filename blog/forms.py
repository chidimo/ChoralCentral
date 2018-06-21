"""Blog Forms"""

from django import forms
from siteuser.models import SiteUser
from song.models import Song
from .models import Post, Comment

class PostShareForm(forms.Form):
    receiving_emails = forms.EmailField(
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : "Enter receiver's email address"}),
    )
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : "Enter your name (optional)"})
    )

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
        super().__init__(*args, **kwargs)
        self.fields['song'].queryset = Song.objects.filter(publish=True)
        
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

    def __init__(self, *args, **kwargs):
        """How to do query in forms"""
        super().__init__(*args, **kwargs)
        self.fields['song'].queryset = Song.objects.filter(publish=True)
        self.fields['song'].initial = self.instance.song

class NewPostFromSongForm(forms.ModelForm):
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

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment", )

        widgets = {
            "comment" : forms.Textarea(
                attrs={'class' : 'form-control comment-box', "placeholder" : "Type your comments."})
        }

class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment", )

        widgets = {
            "comment" : forms.Textarea(
                attrs={'class' : 'form-control', "placeholder" : "Type your comments."})
        }

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment", )

        widgets = {
            "comment" : forms.Textarea(
                attrs={'class' : 'form-control', "placeholder" : "Reply comment."})
        }
    def __init__(self, *args, **kwargs):
        comment_pk = kwargs.pop("comment_pk")
        super(CommentReplyForm, self).__init__(*args, **kwargs)
        comment = Comment.objects.get(pk=comment_pk)
        data = '<quote>'+ comment.comment + '</quote>'
        self.fields['comment'].initial = data

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(
        attrs={'class' : 'form-control', 'placeholder' : "Search posts."}
    ))
