from django.contrib import messages

from rest_framework import viewsets
from ..models import Post, Comment
from .import serializers


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(publish=True).order_by('created')
    serializer_class = serializers.PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created')
    serializer_class = serializers.CommentSerializer

class UserCommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(creator__pk=self.kwargs['pk'])
