"""Requests views"""

from django.views import generic
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin

from siteuser.models import SiteUser
from song.models import Song

from .models import Request, Reply
from .forms import (
    RequestCreateForm, RequestEditForm, ReplyCreateFromRequestForm
    )

class RequestCreate(LoginRequiredMixin, generic.CreateView):
    form_class = RequestCreateForm
    template_name = "request/new.html"

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)
        messages.success(self.request, "Request added successfully.")
        return super(RequestCreate, self).form_valid(form)

class RequestEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Request
    form_class = RequestEditForm
    template_name = "request/edit.html"
    success_message = "Request updated successfully."

class FilterRequests(PaginationMixin, generic.ListView):
    model = Request
    context_object_name = "requests"
    template_name = "request/index.html"
    paginate_by = 25

    def get_queryset(self):
        status = self.request.GET["status"]
        return Request.objects.filter(status=status)

class RequestIndex(PaginationMixin, generic.ListView):
    model = Request
    context_object_name = "requests"
    template_name = "request/index.html"
    paginate_by = 25

class RequestDetail(generic.DetailView):
    model = Request
    context_object_name = "request"
    template_name = "request/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(RequestDetail, self).get_context_data(*args, **kwargs)
        context['answer'] = 'abc'
        return context

class ReplyAddFromRequest(LoginRequiredMixin, generic.CreateView):
    form_class = ReplyCreateFromRequestForm
    context_object_name = "reply_from_request"
    template_name = "request/reply_new_from_request.html"

    def get_form_kwargs(self):
        kwargs = super(ReplyAddFromRequest, self).get_form_kwargs()
        kwargs["pk"] = self.kwargs.get("pk", None)
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)
        self.object = form.save()
        messages.success(self.request, "Request successfully added to {}".format(self.object))
        return super(ReplyAddFromRequest, self).form_valid(form)

class ReplyIndex(PaginationMixin, generic.ListView):
    model = Reply
    context_object_name = "replys"
    template_name = "request/reply_index.html"
    paginate_by = 25

@login_required
def accept_reply(request, request_pk, song_pk):
    request_to_be_answered = Request.objects.get(pk=request_pk)

    if request_to_be_answered.originator.user != request.user:
        messages.error(request, "You're not authorized to accept an answer for this request.")
        return redirect(request_to_be_answered.get_absolute_url())

    song = Song.objects.get(pk=song_pk)
    
    request_to_be_answered.answer = song
    request_to_be_answered.status = True
    request_to_be_answered.save()
    return redirect(request_to_be_answered.get_absolute_url())
