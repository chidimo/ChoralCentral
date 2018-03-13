from rest_framework import viewsets
from ..models import Post, Comment
from .import serializers

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(publish=True).order_by('created')
    serializer_class = serializers.PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created')
    serializer_class = serializers.CommentSerializer