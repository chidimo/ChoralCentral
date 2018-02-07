
"""Views"""

from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models import Count
from django.shortcuts import redirect
from django.template.loader import render_to_string
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
    SiteUserRegistrationForm, SiteUserEditForm, NewRoleForm, RoleEditForm
    )

CustomUser = get_user_model()


class SiteUserIndex(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'siteuser_list'
    template_name = "siteuser/index.html"
    paginate_by = 20

class SiteUserDetail(LoginRequiredMixin, generic.DetailView):
    model = SiteUser
    context_object_name = 'siteuser'
    template_name = "siteuser/detail.html"

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

            new_user = SiteUser(user=user, screen_name=screen_name)
            new_user.save()

            # 2. send email
            activation_link = request.build_absolute_uri(new_user.get_user_creation_url())
            screen_name = new_user.screen_name
            renderer = {'screen_name' : screen_name, 'activation_link' : activation_link}

            subject = "Welcome to ChoralCentral {}.".format(screen_name)
            from_email = settings.EMAIL_HOST_USER

            text_email = render_to_string("welcome_email_template.txt", renderer)
            html_email = render_to_string("welcome_email_template.html", renderer)

            msg = EmailMultiAlternatives(subject, text_email, from_email, [email])
            msg.attach_alternative(html_email, "text/html")
            msg.send()

            return redirect(reverse('siteuser:new_success', args=[screen_name]))
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

class NewRole(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    form_class = NewRoleForm
    template_name = 'siteuser/role_new.html'

class RoleIndex(generic.ListView):
    model = Role
    context_object_name = 'role_list'
    template_name = 'siteuser/role_index.html'
