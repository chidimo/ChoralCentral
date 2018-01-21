
"""Views"""

from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views import generic
from django.shortcuts import render, reverse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin
from .models import SiteUser, Role
from blog.models import Comment
from .forms import (
    SiteUserRegistrationForm, SiteUserEditForm, RoleCreateForm, RoleEditForm
    )

CustomUser = get_user_model()

@login_required
def siteuser_dashboard(request):
    context = {"section" : "dashboard"}
    template = "siteuser/dashboard.html"
    return render(request, template, context)

class SiteUserIndex(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'siteuser_list'
    template_name = "siteuser/index.html"
    paginate_by = 10

class SiteUserDetail(LoginRequiredMixin, generic.DetailView):
    model = SiteUser
    context_object_name = 'siteuser'
    template_name = "siteuser/detail.html"

    def get_context_data(self, **kwargs):
        context = super(SiteUserDetail, self).get_context_data(**kwargs)
        context["last_seen"] = timezone.now()
        return context

class SiteUserComments(PaginationMixin, generic.ListView):
    model = Comment
    context_object_name = 'siteuser_comments'
    template_name = "siteuser/comments.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(SiteUserComments, self).get_context_data(**kwargs)
        context["siteuser"] = SiteUser.objects.get(pk=self.kwargs.get("pk", None))
        return context

    def get_queryset(self):
        creator = SiteUser.objects.get(pk=self.kwargs.get("pk", None))
        return Comment.objects.filter(creator=creator)

def new_siteuser(request):
    template = "siteuser/new.html"
    if request.method == 'POST':
        form = SiteUserRegistrationForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            email = form['email']
            screen_name = form['screen_name']
            password1 = form['password2']
            password2 = form['password2']

            user = CustomUser(email=email)
            user.set_password(password1)

            user.save()

            prof = SiteUser(user=user, screen_name=screen_name)
            prof.save()

            # 2. send email
            activation_link = request.build_absolute_uri(prof.get_user_creation_url())
            send_mail("Welcome to ChoralCentral {}.".format(prof.screen_name),
                      "To activate your account, click this link {}".format(activation_link),
                      settings.EMAIL_HOST_USER,
                      [email],
                      fail_silently=False)
            return HttpResponseRedirect(reverse('siteuser:new_success', args=[prof.screen_name]))
    else:
        form = SiteUserRegistrationForm()
    return render(request, template, {'form' : form})

def welcome_siteuser(request, screen_name):
    template = 'siteuser/new_success.html'
    context = {'screen_name' : screen_name}
    return render(request, template, context)

def activate_siteuser(request, screen_name, pk):
    # check time to see if link has expired.
    user = CustomUser.objects.get(pk=pk)
    context = {}
    if user.is_active:
        siteuser = SiteUser.objects.get(user=user)
        context["active"] = "active"
        context["siteuser"] = siteuser
    else:
        user.is_active = True
        user.save()
        siteuser = SiteUser.objects.get(user=user)
        context["siteuser"] = siteuser
    context["screen_name"] = screen_name
    return render(request, "siteuser/new_activation.html", context)

class SiteUserEdit(LoginRequiredMixin, generic.UpdateView):
    model = SiteUser
    form_class = SiteUserEditForm
    template_name = 'siteuser/edit.html'

class RoleCreate(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    form_class = RoleCreateForm
    template_name = 'siteuser/role_new.html'

class RoleIndex(generic.ListView):
    model = Role
    context_object_name = 'role_list'
    template_name = 'siteuser/role_index.html'
