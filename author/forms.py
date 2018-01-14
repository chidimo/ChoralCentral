"""Forms"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Author

class NewAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("author_type", "first_name", "last_name", "bio")

        widgets = {
            "first_name" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "First Name"}),
            "last_name" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Last Name"}),
            "bio" : forms.Textarea(
                attrs={'rows' : 5, 'columns' : 10, 'class' : 'form-control', 'placeholder' : "Biography (optional)"}),
            "author_type" : forms.Select(
                attrs={'class' : 'form-control'})
        }

class AuthorEditForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("author_type", "first_name", "last_name", "bio")

        widgets = {
            "first_name" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "First Name"}),
            "last_name" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Last Name"}),
            "bio" : forms.Textarea(
                attrs={'rows' : 5, 'columns' : 10, 'class' : 'form-control', 'placeholder' : "Biography (optional)"}),
            "author_type" : forms.Select(
                attrs={'class' : 'form-control'})
        }
