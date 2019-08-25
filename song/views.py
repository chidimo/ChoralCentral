from collections import OrderedDict

from django.http import JsonResponse, HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Voicing, Language, Season, MassPart, Song
from .serializers import SongSerializer, MassPartSerializer, SeasonSerializer, LanguageSerializer, VoicingSerializer

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})

class VoicesViewSet(viewsets.ModelViewSet):
    queryset = Voicing.objects.all()
    serializer_class = VoicingSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})

class MassPartViewSet(viewsets.ModelViewSet):
    queryset = MassPart.objects.all()
    serializer_class = MassPartSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})

class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})
