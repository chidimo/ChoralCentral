
"""Views"""

import uuid

from django.db import IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views import generic
from django.shortcuts import render, reverse, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# from django.contrib.auth.models import Group, Permission

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin
from social_django.models import UserSocialAuth

from .models import SiteUser, Role, SiteUserGroup, GroupMembership, GroupJoinRequest, Follow
from blog.models import Comment
from song.forms import ShareForm
from song.models import Song
from blog.models import Post, Comment

from .forms import (
    SiteUserRegistrationForm, SiteUserEditForm, NewRoleForm, RoleEditForm,
    NewSiteUserGroupForm
)

CustomUser = get_user_model()

def get_api_key(request):
    siteuser = request.user.siteuser
    if siteuser.key:
        msg = "You already have an API key"
    else:
        siteuser.key = uuid.uuid4()
        siteuser.save(update_fields=['key'])
        msg = "Your API key is {}".format(siteuser.key)
    messages.success(request, msg)
    return redirect(reverse("siteuser:detail", kwargs={"pk" : siteuser.pk, "slug" : siteuser.slug}))

def reset_api_key(request):
    siteuser = request.user.siteuser
    siteuser.key = uuid.uuid4()
    siteuser.save(update_fields=['key'])
    msg = "Your new API key is {}. Don't forget to update your applications".format(siteuser.key)
    messages.warning(request, msg)
    return redirect(reverse("siteuser:detail", kwargs={"pk" : siteuser.pk, "slug" : siteuser.slug}))

class SiteUserIndex(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'siteuser_list'
    template_name = "siteuser/index.html"
    paginate_by = 20

class UserDetail(generic.DetailView):
    model = SiteUser
    context_object_name = 'siteuser'
    template_name = "siteuser/detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        context["share_form"] = ShareForm()
        return context

class SongLoveBirds(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'song_love_birds'
    template_name = 'siteuser/love_birds_song.html'
    paginate_by = 24

    def get_queryset(self):
        song = Song.objects.get(pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        return song.likes.all()

    def get_context_data(self, *args):
        context = super(SongLoveBirds, self).get_context_data(*args)
        context['song'] = Song.objects.get(pk=self.kwargs['pk'])
        return context

class PostLoveBirds(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'post_love_birds'
    template_name = 'siteuser/love_birds_post.html'
    paginate_by = 24

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        return post.likes.all()

    def get_context_data(self, *args):
        context = super(PostLoveBirds, self).get_context_data(*args)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        return context

class CommentLoveBirds(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'comment_love_birds'
    template_name = 'siteuser/love_birds_comment.html'
    paginate_by = 24

    def get_queryset(self):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        return comment.likes.all()

    def get_context_data(self, *args):
        context = super(CommentLoveBirds, self).get_context_data(*args)
        context['comment'] = Comment.objects.get(pk=self.kwargs['pk'])
        return context

class UserComments(PaginationMixin, generic.ListView):
    model = Comment
    context_object_name = 'user_comments'
    template_name = "siteuser/comments.html"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(UserComments, self).get_context_data(**kwargs)
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
            email = form['email'].strip()
            screen_name = form['screen_name'].strip()
            password1 = form['password1'].strip()
            # password2 = form['password2']

            user = CustomUser(email=email)
            user.set_password(password1)
            user.save()

            new_user = SiteUser(user=user, screen_name=screen_name)
            new_user.save()

            # 2. send email
            activation_link = request.build_absolute_uri(new_user.get_user_creation_url())
            screen_name = new_user.screen_name
            context = {'screen_name' : screen_name, 'activation_link' : activation_link}

            subject = "Welcome to ChoralCentral {}.".format(screen_name)
            from_email = settings.EMAIL_HOST_USER

            text_email = render_to_string("welcome_email_template.txt", context)
            html_email = render_to_string("welcome_email_template.html", context)

            msg = EmailMultiAlternatives(subject, text_email, from_email, [email, "choralcentral@gmail.com"])
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

class SiteUserEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = SiteUser
    form_class = SiteUserEditForm
    template_name = 'siteuser/edit.html'
    success_message = "Profile updated successfully."

class NewRole(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    form_class = NewRoleForm
    template_name = 'siteuser/role_new.html'
    success_message = "New role added successfully"

class RoleIndex(generic.ListView):
    model = Role
    context_object_name = 'role_list'
    template_name = 'siteuser/role_index.html'

# https://docs.djangoproject.com/en/2.0/topics/db/models/

class NewSiteUserGroup(LoginRequiredMixin, generic.CreateView):
    form_class = NewSiteUserGroupForm
    template_name = 'siteuser/new_siteuser_group.html'

    def form_valid(self, form):
        self.object = form.save()

        initial_group_member = GroupMembership(
            siteuser=SiteUser.objects.get(user=self.request.user),
            group = self.object,
            is_group_admin=True)

        messages.success(self.request, "Your group was created successfully.")
        return redirect(self.get_absolute_url())

@login_required
def social_management(request):
    template = "siteuser/social_management.html"
    context = {}
    user = request.user

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        yahoo_login = user.social_auth.get(provider='yahoo-oauth2')
    except UserSocialAuth.DoesNotExist:
        yahoo_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    context['facebook_login'] = facebook_login
    context['google_login'] = google_login
    context['twitter_login'] = twitter_login
    context['yahoo_login'] = yahoo_login
    context['can_disconnect'] = can_disconnect
    return render(request, template, context)

@login_required
def social_password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            login(request, request.user, backend='django.contrib.auth.backends.ModelBackend',)
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'siteuser/social_password_change_form.html', {'form': form})

