
"""Views"""

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
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# from django.contrib.auth.models import Group, Permission

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin
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


