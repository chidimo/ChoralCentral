from django.db.models import Q

from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(publish=True).order_by('created')
    serializer_class = serializers.PostSerializer
