"""views"""

from django.db.models import Count
from django.views import generic
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django_addanother.views import CreatePopupMixin
from django.urls import reverse_lazy

from pure_pagination.mixins import PaginationMixin

import rules
from rules.contrib.views import PermissionRequiredMixin

from siteuser.models import SiteUser, SiteUserPermission

from .models import Author
from .forms import AuthorEditForm, NewAuthorForm
from .predicates import CONTEXT_MESSAGES

class AuthorIndex(PaginationMixin, generic.ListView):
    model = Author
    context_object_name = 'authors'
    template_name = "author/index.html"
    paginate_by = 20

    def get_queryset(self):
        return Author.objects.annotate(Count("song__publish")).order_by("-song__publish__count")

class AuthorDetail(LoginRequiredMixin, generic.ListView):
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
        form.instance.creator = self.request.user.siteuser
        return super(NewAuthor, self).form_valid(form)

class AuthorEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Author
    form_class = AuthorEditForm
    template_name = 'author/edit.html'
    success_message = "Author updated successfully."

    def get(self, request, *args, **kwargs):
        """Check that the object to be edited belongs to user that created it"""
        self.object = self.get_object()
        if rules.test_rule('edit_author', self.request.user, self.object):
            return self.render_to_response(self.get_context_data())
        messages.error(self.request, CONTEXT_MESSAGES['OPERATION_FAILED'])
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('siteuser:library', kwargs={'pk' : self.request.user.siteuser.pk, 'slug' : self.request.user.siteuser.slug})

class DeleteAuthor(SuccessMessageMixin, generic.DeleteView):
    model = Author
    template_name = "author/delete.html"
    success_message = "Author deleted successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_songs'] = Author.objects.get(pk=self.kwargs['pk']).song_set.all()
        return context
    
    def get_success_url(self):
        return reverse('siteuser:library', kwargs={'pk' : self.request.user.siteuser.pk, 'slug' : self.request.user.siteuser.slug})

    def get(self, request, *args, **kwargs):
        """Check that the object to be edited belongs to user that created it"""
        self.object = self.get_object()
        if rules.test_rule('edit_author', self.request.user, self.object):
            return self.render_to_response(self.get_context_data())
        messages.error(self.request, CONTEXT_MESSAGES['OPERATION_FAILED'])
        return redirect(self.get_success_url())
