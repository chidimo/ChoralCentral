"""views"""

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django_addanother.views import CreatePopupMixin

from .forms import NewVoicingForm, EditVoicingForm
from siteuser.models import SiteUser

class CreateVoicing(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    form_class = NewVoicingForm
    template_name = "voicing/new.html"

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)
        return super(CreateVoicing, self).form_valid(form)

class VoicingEdit(LoginRequiredMixin, generic.UpdateView):
    form_class = EditVoicingForm
    template_name = 'voicing/edit.html'
