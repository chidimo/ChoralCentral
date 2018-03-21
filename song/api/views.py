from django.db.models import Q

from rest_framework import viewsets

from ..models import Song
from . import serializers

class PublishedSongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.filter(Q(publish=True)).order_by('created')
    serializer_class = serializers.SongSerializer

class UnpublishedSongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.filter(Q(publish=False)).order_by('created')
    serializer_class = serializers.SongSerializer

class PublishedAuthorSongViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SongSerializer

    def get_queryset(self):
        query = Q(authors__pk__in=[self.kwargs['pk']]) & Q(publish=True)
        return Song.objects.filter(query).order_by('created')
