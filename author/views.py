"""views"""

from django.db.models import Count
from django.views import generic
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
        return Author.objects.all().annotate(Count("song__publish")).order_by("-song__publish__count")

class AuthorAdd(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    form_class = NewAuthorForm
    template_name = 'author/new.html'

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)
        return super(AuthorAdd, self).form_valid(form)

class AuthorEdit(LoginRequiredMixin, generic.UpdateView):
    model = Author
    form_class = AuthorEditForm
    template_name = 'author/edit.html'

class AuthorDetail(generic.DetailView):
    model = Author
    context_object_name = 'author'
    template_name = 'author/detail.html'

    # def get_object(self):
    #     author = Author.objects.get(pk=self.kwargs.get("pk", None))
    #     return author

class DeleteAuthor(generic.DeleteView):
    model = Author
    success_url = reverse_lazy('song:index')
    template_name = "confirm_delete.html"
