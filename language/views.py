"""views"""

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django_addanother.views import CreatePopupMixin
from django.urls import reverse_lazy

from .models import Language
from .forms import NewLanguageForm, EditLanguageForm

class LanguageIndex(generic.ListView):
    template_name = "language/index.html"
    context_object_name = 'languages'
    model = Language

class LanguageCreate(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    form_class = NewLanguageForm
    template_name = 'language/new.html'

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)
        return super(LanguageAdd, self).form_valid(form)

class LanguageEdit(LoginRequiredMixin, generic.CreateView):
    form_class = NewLanguageForm
    template_name = 'language/new.html'

class LanguageDetail(generic.DetailView):
    model = Language
    context_object_name = 'language'
    template_name = 'language/detail.html'

class LanguageDelete(generic.DeleteView):
    model = Language
    success_url = reverse_lazy('song:language_index')
    template_name = "confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super(LanguageDeleteDelete, self).get_context_data(**kwargs)
        context["which_model"] = "language"
        return context
