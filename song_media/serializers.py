from rest_framework import serializers

from .models import VocalPart, ScoreNotation, Score, Midi, VideoLink
from author.serializers import AuthorSerializer
from siteuser.serializers import SiteUserSerializer

class VocalPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = VocalPart
        fields = ('name', )

class ScoreNotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreNotation
        fields = ('name', )

class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Score
        fields = ('creator', )

class MidiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Midi
        fields = ('creator', )

class VideoLinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoLink
        fields = ('creator', )
