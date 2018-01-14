"""forms"""

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Voicing

class NewVoicingForm(forms.ModelForm):
    class Meta:
        model = Voicing
        fields = ("voicing", )

        widgets = {
            "voicing" : forms.TextInput(
                attrs={'class' : 'form-control', 'placeholder' : "Voicing"})
        }

    def clean_voicing(self):
        voicing = self.cleaned_data.get("voicing", None).upper()
        if Voicing.objects.filter(voicing=voicing).exists():
            raise forms.ValidationError(_("{} already exists".format(voicing)))
        return voicing

class EditVoicingForm(forms.ModelForm):
    class Meta:
        model = Voicing
        fields = ("voicing", )
