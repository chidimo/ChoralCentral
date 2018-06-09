"""views"""

from django.db.models import Count
from django.views import generic
# from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django_addanother.views import CreatePopupMixin
from django.urls import reverse_lazy

from siteuser.models import SiteUser

from pure_pagination.mixins import PaginationMixin

from .models import Author
from .forms import AuthorEditForm, NewAuthorForm

class AuthorIndex(PaginationMixin, generic.ListView):
    model = Author
    context_object_name = 'authors'
    template_name = "author/index.html"
    paginate_by = 25

    def get_queryset(self):
        return Author.objects.annotate(Count("song__publish")).order_by("-song__publish__count")

class AuthorDetail(generic.ListView):
    model = Author
    context_object_name = 'author_songs'
    template_name = 'author/detail.html'

    def author(self):
        return Author.objects.get(pk=self.kwargs['pk'], slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        context['author'] = self.author()
        return context

    def get_queryset(self):
        return self.author().song_set.all().filter(publish=True)

class NewAuthor(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    form_class = NewAuthorForm
    template_name = 'author/new.html'
    success_message = "Author added successfully."

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)
        return super(NewAuthor, self).form_valid(form)

class AuthorEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Author
    form_class = AuthorEditForm
    template_name = 'author/edit.html'
    success_message = "Author updated successfully."

class DeleteAuthor(SuccessMessageMixin, generic.DeleteView):
    model = Author
    success_url = reverse_lazy('song:index')
    template_name = "confirm_delete.html"
    success_message = "Author deleted successfully."
