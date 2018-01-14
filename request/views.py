"""Requests views"""

from django import forms
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin

from siteuser.models import SiteUser
from .models import Request, Reply
from . import forms as fm

class RequestCreate(LoginRequiredMixin, generic.CreateView):
    form_class = fm.RequestCreateForm
    template_name = "request/new.html"

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)
        return super(RequestCreate, self).form_valid(form)

class RequestEdit(LoginRequiredMixin, generic.UpdateView):
    model = Request
    form_class = fm.RequestEditForm
    template_name = "request/edit.html"

class FilterRequests(PaginationMixin, generic.ListView):
    model = Request
    context_object_name = "requests"
    template_name = "request/index.html"
    paginate_by = 20

    def get_queryset(self):
        status = self.request.GET["status"]
        return Request.objects.filter(status=status)

class RequestIndex(PaginationMixin, generic.ListView):
    model = Request
    context_object_name = "requests"
    template_name = "request/index.html"
    paginate_by = 20

class RequestDetail(generic.DetailView):
    model = Request
    context_object_name = "request"
    template_name = "request/detail.html"

class ReplyAddFromRequest(LoginRequiredMixin, generic.CreateView):
    context_object_name = "reply_from_request"
    form_class = fm.ReplyCreateFromRequestForm
    template_name = "request/reply_new_from_request.html"

    def get_form_kwargs(self):
        kwargs = super(ReplyAddFromRequest, self).get_form_kwargs()
        kwargs["pk"] = self.kwargs.get("pk", None)
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.originator = SiteUser.objects.get(user=self.request.user)
        return super(ReplyAddFromRequest, self).form_valid(form)

class ReplyIndex(PaginationMixin, generic.ListView):
    model = Reply
    context_object_name = "replys"
    template_name = "request/reply_index.html"

