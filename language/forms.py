"""Forms"""

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Language

class NewLanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ("language", )

        widgets = {
            "language" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Language"})
        }

    def clean_language(self):
        language = self.cleaned_data.get("language", None).upper()
        if Language.objects.filter(language=language):
            raise forms.ValidationError(_("{} already exists".format(language)))

class EditLanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ("language",)
