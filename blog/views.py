"""Docstring"""
import json

from django.views import generic
from django.conf import settings
from django.http import HttpResponse, JsonResponse
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

from .utils import star_or_unstar_object
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
        return super().form_valid(form)

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
        return super().form_valid(form)

class PostIndex(PaginationMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/index.html"
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.select_related('song', 'creator').filter(publish=True)

    def get_context_data(self):
        context = super().get_context_data()
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
        context = super().get_context_data(**kwargs)
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

    # Handle comment post via ajax
    if request.method == 'POST':
        if request.is_ajax():

            like_what = request.POST.get('like_what', None)
            
            if like_what == 'comment':
                pk  = int(request.POST.get('pk')) # need to send this since I have multiple like buttons on this page
                model = request.POST.get('model')
                app_label = request.POST.get('app_label')
                siteuser = request.user.siteuser
                data = star_or_unstar_object(siteuser, pk, app_label, model)
                return JsonResponse(data)
            elif like_what is None:
                comment = request.POST.get('comment')
                siteuser = request.user.siteuser
                post = Post.objects.get(pk=pk, slug=slug)
                comm = Comment.objects.create(creator=siteuser, post=post, comment=comment)
                comm.likes.add(siteuser)
                comm.like_count = comm.likes.count()
                comm.save(update_fields=['like_count'])

                data = {'success' : True, 'message' : 'Your comment was successfully added'}
                return JsonResponse(data)
            elif like_what == 'post':
                siteuser = request.user.siteuser
                data = star_or_unstar_object(siteuser, pk, 'blog', 'post')
                return JsonResponse(data)
            else:
                pass

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

class ReplyComment(LoginRequiredMixin, generic.CreateView):
    context_object_name = 'comment'
    form_class = CommentReplyForm
    template_name = "blog/comment_reply.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
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
        return super().form_valid(form)

class DeleteComment(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'

def share_post_by_mail(request, pk, slug):
    context = {}

    from_email = settings.EMAIL_HOST_USER

    if request.method == 'GET':
        post = Post.objects.get(pk=pk, slug=slug)

        subject = 'Post share from ChoralCentral'.format(post.title)
        context['post'] = post
        context['post_link'] = request.build_absolute_uri(post.get_absolute_url())

        form = PostShareForm(request.GET)
        if form.is_valid():
            form = form.cleaned_data
            receiving_email = form['receiving_email']
            name = form['name']
            context['name'] = name

            text_email = render_to_string("blog/share_post_by_mail.txt", context)
            html_email = render_to_string("blog/share_post_by_mail.html", context)

            msg = EmailMultiAlternatives(subject, text_email, from_email, [receiving_email])
            msg.attach_alternative(html_email, "text/html")
            msg.send()
            messages.success(request, "Post was successfully sent to {}".format(receiving_email))
            return redirect(post.get_absolute_url())
        else:
            messages.error(request, "Invalid email.")
            return redirect(post.get_absolute_url())
