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
                attrs={'class' : 'form-control', 'placeholder' : "Biography (optional)"}),
            "author_type" : forms.Select(
                attrs={'class' : 'form-control'})
        }

    def clean(self):
        data = super().clean()
        # print('author cleaned data', data)
        first_name = data['first_name'].lower()
        last_name = data['last_name'].lower()
        author_type = data['author_type'].lower()

        try:
            Author.objects.get(first_name=first_name, last_name=last_name)
            msg = 'Author named {} {} already exists.'.format(first_name, last_name)
            self.add_error('first_name', msg)
        except Author.DoesNotExist:
            pass

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
                attrs={'class' : 'form-control', 'placeholder' : "Biography (optional)"}),
            "author_type" : forms.Select(
                attrs={'class' : 'form-control'})
        }
