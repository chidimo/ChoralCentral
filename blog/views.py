"""Docstring"""
import json

from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin
from algoliasearch_django import get_adapter

from siteuser.models import SiteUser
from song.models import Song

from .models import Post, Comment
from .forms import (
    PostShareForm, NewPostForm, PostEditForm,
    PostCreateFromSongForm, CommentCreateForm,
    CommentEditForm, CommentReplyForm
)

# pylint: disable=R0901, C0111

def instant_blog(request):
    context = {}
    context['appID'] = settings.ALGOLIA['APPLICATION_ID']
    context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
    context['indexName'] = get_adapter(Post).index_name
    context['posts'] = Post.objects.filter(publish=True)
    return render(request, 'blog/instant_blog.html', context)

def auto_blog(request):
    context = {}
    context['appID'] = settings.ALGOLIA['APPLICATION_ID']
    context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
    context['indexName'] = get_adapter(Post).index_name
    return render(request, 'blog/autocomplete_blog.html', context)

@login_required
@require_POST
def post_like_view(request):
    if request.method == 'POST':
        user = SiteUser.objects.get(user=request.user)
        pk = request.POST.get('pk', None)
        post = get_object_or_404(Post, pk=pk)

        if post.likes.filter(pk=user.pk).exists():
            post.likes.remove(user)
            post.like_count = post.likes.count()
            post.save(update_fields=['like_count'])
            message = "You unstarred this post.\n {} now has {} stars".format(post.title, post.like_count)
        else:
            post.likes.add(user)
            post.like_count = post.likes.count()
            post.save(update_fields=['like_count'])
            message = "You starred this post.\n {} now has {} stars".format(post.title, post.like_count)
    context = {'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

class PostCreate(LoginRequiredMixin, generic.CreateView):
    context_object_name = 'post'
    template_name = 'blog/new.html'
    form_class = NewPostForm

    def get_form_kwargs(self):
        """include 'user' and 'pk' in the kwargs to be sent to form"""
        kwargs = super(PostCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.creator = SiteUser.objects.get(user=self.request.user)
        self.object = form.save()
        self.object.likes.add(SiteUser.objects.get(user=self.request.user))

        self.object.like_count = self.object.likes.count()
        self.object.save(update_fields=['like_count'])
        messages.success(self.request, "Post created successfully !")
        return super(PostCreate, self).form_valid(form)

class PostCreateFromSong(LoginRequiredMixin, generic.CreateView):
    form_class = PostCreateFromSongForm
    context_object_name = 'post'
    template_name = 'blog/new.html'

    def form_valid(self, form):
        form.instance.creator = SiteUser.objects.get(user=self.request.user)
        form.instance.song = Song.objects.get(pk=self.kwargs["pk"])

        self.object = form.save()
        self.object.likes.add(SiteUser.objects.get(user=self.request.user))

        self.object.like_count = self.object.likes.count()
        self.object.save(update_fields=['like_count'])
        messages.success(self.request, "Post successfully created for song {}".format(self.object.song.title))
        return super(PostCreateFromSong, self).form_valid(form)

class PostIndex(PaginationMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/index.html"
    paginate_by = 25

    def get_queryset(self):
        return Post.objects.filter(publish=True)

    def get_context_data(self):
        context = super(PostIndex, self).get_context_data()
        context['share_form'] = PostShareForm()
        return context

class PostDetail(PaginationMixin, generic.ListView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "comments"
    paginate_by = 25

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs.get("pk", None))
        return Comment.objects.filter(post=post)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context["comment_form"] = CommentCreateForm()
        context['post_share_form'] = PostShareForm()
        context["post"] = Post.objects.get(pk=self.kwargs.get("pk", None))
        return context

class PostEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = "blog/edit.html"
    success_message = "Post updated successfully !"

    def get_form_kwargs(self):
        """include 'user' and 'pk' in the kwargs to be sent to form"""
        kwargs = super(PostEdit, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class EditComment(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Comment
    form_class = CommentEditForm
    template_name = "blog/edit_comment.html"
    success_message = "Comment updated successfully"

class CommentCreate(LoginRequiredMixin, generic.CreateView):
    context_object_name = 'comment'
    form_class = CommentCreateForm
    template_name = 'blog/comment_new.html'

    def get_success_url(self):
        post = self.object.post
        pagination = PostDetail().paginate_by
        post_url = reverse('blog:detail', kwargs={'pk' : post.pk, 'slug' : post.slug})
        number_of_comments = post.comment_set.count()

        pages = number_of_comments // pagination # get whole pages
        remainder_comments = number_of_comments % pagination
        if remainder_comments: # check for remainder
            pages += 1
        comment_page = '?page={}'.format(pages)
        comment_target_id = '#{}'.format(remainder_comments-1)
        return post_url + comment_page + comment_target_id

    def form_valid(self, form):
        form.instance.creator = SiteUser.objects.get(user=self.request.user)
        form.instance.post = Post.objects.get(pk=self.kwargs["pk"])

        self.object = form.save()
        self.object.likes.add(SiteUser.objects.get(user=self.request.user))

        self.object.like_count = self.object.likes.count()
        self.object.save(update_fields=['like_count'])
        messages.success(self.request, "Comment successfully created !")
        return super(CommentCreate, self).form_valid(form)

    def get_context_data(self, *args):
        context = super(CommentCreate, self).get_context_data(*args)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        return context

class ReplyComment(LoginRequiredMixin, generic.CreateView):
    context_object_name = 'comment'
    form_class = CommentReplyForm
    template_name = "blog/comment_reply.html"

    def get_form_kwargs(self):
        kwargs = super(ReplyComment, self).get_form_kwargs()
        kwargs['comment_pk'] = self.kwargs['comment_pk']
        return kwargs

    def form_valid(self, form):
        form.instance.creator = SiteUser.objects.get(user=self.request.user)
        form.instance.post = Post.objects.get(pk=self.kwargs["post_pk"])

        self.object = form.save()
        self.object.likes.add(SiteUser.objects.get(user=self.request.user))

        self.object.like_count = self.object.likes.count()
        self.object.save(update_fields=['like_count'])
        messages.success(self.request, "Reply successfully created.")
        return super(ReplyComment, self).form_valid(form)

class DeleteComment(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'

def share_post_by_mail(request, pk, slug):
    context = {}

    from_email = settings.EMAIL_HOST_USER

    if request.method == 'GET':
        post = Post.objects.get(pk=pk, slug=slug)

        subject = '{} was shared with you from ChoralCentral'.format(post.title)
        context['post'] = post
        context['post_link'] = request.build_absolute_uri(post.get_absolute_url())

        form = PostShareForm(request.GET)
        if form.is_valid():
            form = form.cleaned_data
            receiving_emails = form['receiving_emails']
            name = form['name']
            context['name'] = name

            email_list = [each.strip() for each in receiving_emails.split(',')]
            if len(email_list) > 5:
                messages.error(request, "Too many emails. Please enter at most 5 email addresses.")
                return redirect(post.get_absolute_url())

            for email in email_list:
                text_email = render_to_string("blog/share_post_by_mail.txt", context)
                html_email = render_to_string("blog/share_post_by_mail.html", context)

                msg = EmailMultiAlternatives(subject, text_email, from_email, [email])
                msg.attach_alternative(html_email, "text/html")
                msg.send()

    success_msg = "Post was successfully sent to {}".format(", ".join(email_list))
    messages.success(request, success_msg)
    return redirect(post.get_absolute_url())
