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
from redirect301.models import Url301

from .models import Post, Comment
from .forms import (
    PostShareForm, NewPostForm, PostEditForm,
    NewPostFromSongForm, NewCommentForm,
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

class NewPost(LoginRequiredMixin, generic.CreateView):
    context_object_name = 'post'
    template_name = 'blog/new.html'
    form_class = NewPostForm

    def form_valid(self, form):
        siteuser = self.request.user.siteuser
        form.instance.creator = siteuser
        self.object = form.save()
        self.object.likes.add(siteuser)

        self.object.like_count = self.object.likes.count()
        self.object.save(update_fields=['like_count'])
        messages.success(self.request, "Post created successfully !")
        return super(NewPost, self).form_valid(form)

class NewPostFromSong(LoginRequiredMixin, generic.CreateView):
    form_class = NewPostFromSongForm
    context_object_name = 'post'
    template_name = 'blog/new.html'

    def form_valid(self, form):
        siteuser = self.request.user.siteuser
        form.instance.creator = siteuser
        form.instance.song = Song.objects.get(pk=self.kwargs["pk"])

        self.object = form.save()
        self.object.likes.add(siteuser)

        self.object.like_count = self.object.likes.count()
        self.object.save(update_fields=['like_count'])
        messages.success(self.request, "Post successfully created for song {}".format(self.object.song.title))
        return super(NewPostFromSong, self).form_valid(form)

class PostIndex(PaginationMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/index.html"
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.select_related('song', 'creator').filter(publish=True)

    def get_context_data(self):
        context = super(PostIndex, self).get_context_data()
        context['share_form'] = PostShareForm()
        return context

class PostDetail(PaginationMixin, generic.ListView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "comments"
    paginate_by = 20

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs.get("pk", None))
        return Comment.objects.filter(post=post)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context["comment_form"] = NewCommentForm()
        context['post_share_form'] = PostShareForm()
        context["post"] = Post.objects.get(pk=self.kwargs.get("pk", None))
        return context

def post_redirect_301_view(request, pk, slug):
    template = '301.html'
    context = {}
    context['object'] = Post.objects.select_related('creator').get(pk=pk, slug=slug)
    return render(request, template, context)

def post_detail_view(request, pk, slug):
    template = 'blog/detail.html'
    context = {}
    context['post_share_form'] = PostShareForm()
    context["comment_form"] = NewCommentForm()
    try:
        post = Post.objects.select_related('creator').get(pk=pk, slug=slug)
        context['post'] = post
        return render(request, template, context)
    except Post.DoesNotExist:
        # the url pointed to may have itself moved. So we work in a loop till we possibly find a match
        old_ref = slug
        while True:
            # There's a match in the url mapping table. Now we have to check if the song pointed to still exists
            try:
                ref = Url301.objects.get(app_name="blog", old_reference=old_ref).new_reference
                try:
                    Post.objects.select_related('creator').get(pk=pk, slug=ref)
                    return redirect(reverse('blog:post_moved', kwargs={'pk' : pk, 'slug' : ref}))
                except Post.DoesNotExist:
                    old_ref = ref
            # there is no match in the url mapping table. We're done
            except Url301.DoesNotExist:
                raise(Post.DoesNotExist)

class PostEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = "blog/edit.html"
    success_message = "Post updated successfully."

    def get_success_url(self):
        return reverse('siteuser:library', kwargs={'pk' : self.request.user.siteuser.pk, 'slug' : self.request.user.siteuser.slug})

    # def get(self, request, *args, **kwargs):
    #     self.object = Song.objects.get(pk=self.kwargs["pk"])
    #     if rules.test_rule('edit_song', self.request.user, self.object):
    #         return self.render_to_response(self.get_context_data())
    #     messages.error(self.request, CONTEXT_MESSAGES['OPERATION_FAILED'])
    #     return redirect(self.get_success_url())

    def form_valid(self, form):
        old_ref = Post.objects.get(pk=self.kwargs["pk"]).slug
        self.object = form.save()
        new_ref = self.object.slug

        print("new: ", new_ref, "old: ", old_ref)

        # map the old refrence to a new one
        if old_ref != new_ref:
            print("not equal")
            redirect_url = Url301.objects.create(app_name="blog", old_reference=old_ref, new_reference=new_ref)

        messages.success(self.request, "Song was successfully updated")
        return redirect(self.get_success_url())

class EditComment(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Comment
    form_class = CommentEditForm
    template_name = "blog/comment_edit.html"
    success_message = "Comment updated successfully"

class NewComment(LoginRequiredMixin, generic.CreateView):
    context_object_name = 'comment'
    form_class = NewCommentForm
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
        siteuser = self.request.user.siteuser
        form.instance.creator = siteuser
        form.instance.post = Post.objects.get(pk=self.kwargs["pk"])
        self.object = form.save()

        self.object.likes.add(siteuser)
        self.object.like_count = self.object.likes.count()
        self.object.save(update_fields=['like_count'])
        messages.success(self.request, "Comment successfully created !")
        return super(NewComment, self).form_valid(form)

    def get_context_data(self, *args):
        context = super(NewComment, self).get_context_data(*args)
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
        siteuser = self.request.user.siteuser
        form.instance.creator = siteuser
        form.instance.post = Post.objects.get(pk=self.kwargs["post_pk"])
        self.object = form.save()

        self.object.likes.add(siteuser)
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
            if len(email_list) > 3:
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
