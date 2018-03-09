"""Docstring"""

from django.views import generic
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin
from algoliasearch_django import get_adapter

from siteuser.models import SiteUser
from song.models import Song
from song.forms import ShareForm

from .models import Post, Comment
from .forms import NewPostForm, PostEditForm, PostCreateFromSongForm, CommentCreateForm, CommentEditForm, CommentNumberForm

# pylint: disable=R0901, C0111

def instant_blog(request):
    context = {}
    context['appID'] = settings.ALGOLIA['APPLICATION_ID']
    context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
    context['indexName'] = get_adapter(Post).index_name
    context['posts'] = Post.published_set.all()
    return render(request, 'blog/instant_blog.html', context)

def auto_blog(request):
    context = {}
    context['appID'] = settings.ALGOLIA['APPLICATION_ID']
    context['searchKey'] = settings.ALGOLIA['SEARCH_API_KEY']
    context['indexName'] = get_adapter(Post).index_name
    return render(request, 'blog/autocomplete_blog.html', context)

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
        return super(PostCreateFromSong, self).form_valid(form)

class PostIndex(PaginationMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/index.html"
    paginate_by = 30

    def get_queryset(self):
        return Post.published_set.all()

    def get_context_data(self):
        context = super(PostIndex, self).get_context_data()
        context['share_form'] = ShareForm()
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
        context["comment_form"] = CommentCreateForm()
        context["post"] = Post.objects.get(pk=self.kwargs.get("pk", None))
        return context

class PostEdit(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = "blog/edit.html"

class EditComment(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    form_class = CommentEditForm
    template_name = "blog/comment_edit.html"

class CommentCreate(LoginRequiredMixin, generic.CreateView):
    context_object_name = 'comment'
    form_class = CommentCreateForm

    def form_valid(self, form):
        form.instance.creator = SiteUser.objects.get(user=self.request.user)
        form.instance.post = Post.objects.get(pk=self.kwargs.get("pk", None))

        self.object = form.save()
        self.object.likes.add(SiteUser.objects.get(user=self.request.user))
        return super(CommentCreate, self).form_valid(form)

def share_by_mail(request, pk, slug):
    context = {}
    post = Post.objects.get(pk=pk, slug=slug)
    sharer = request.user.siteuser.screen_name
    from_email = settings.EMAIL_HOST_USER
    subject = '{} from {}'.format(post.title, sharer)
    context['post'] = post
    context['sharer'] = sharer
    context['post_link'] = request.build_absolute_uri(post.get_absolute_url())

    if request.method == 'GET':
        form = ShareForm(request.GET)
        if form.is_valid():
            form = form.cleaned_data
            email = form['email']

    text_email = render_to_string("blog/share_by_mail.txt", context)
    html_email = render_to_string("blog/share_by_mail.html", context)

    msg = EmailMultiAlternatives(subject, text_email, from_email, [email])
    msg.attach_alternative(html_email, "text/html")
    msg.send()
    return redirect('blog:index')
