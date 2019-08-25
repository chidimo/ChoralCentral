from collections import OrderedDict

from django.http import JsonResponse, HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response

from .models import VocalPart, ScoreNotation, Score, Midi, VideoLink
from .serializers import VocalPartSerializer, ScoreNotationSerializer, ScoreSerializer, MidiSerializer, VideoLinkSerializer

class VocalPartViewSet(viewsets.ModelViewSet):
    queryset = VocalPart.objects.all()
    serializer_class = VocalPartSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})

class ScoreNotationViewSet(viewsets.ModelViewSet):
    queryset = ScoreNotation.objects.all()
    serializer_class = ScoreNotationSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})

class MidiViewSet(viewsets.ModelViewSet):
    queryset = Midi.objects.all()
    serializer_class = MidiSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})

class VideoLinkViewSet(viewsets.ModelViewSet):
    queryset = VideoLink.objects.all()
    serializer_class = VideoLinkSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})
