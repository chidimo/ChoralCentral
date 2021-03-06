from rest_framework import serializers

from ..models import Voicing, Language, Season, MassPart, Song
from author.api.serializers import AuthorSerializer
from siteuser.api.serializers import SiteUserSerializer

class VoicingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voicing
        fields = ('name', )

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('name', )

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ('name', )

class MassPartSerializer(serializers.ModelSerializer):
    part = serializers.CharField(source='__str__', read_only=True)
    class Meta:
        model = MassPart
        fields = ('name', )

class SongSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    creator = SiteUserSerializer()
    voicing = VoicingSerializer()
    language = LanguageSerializer()
    seasons = SeasonSerializer(many=True, read_only=True)
    mass_parts = MassPartSerializer(many=True, read_only=True)
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = (
            'creator', 'title', 'scripture_reference', 'lyrics', 'voicing',
            'language', 'seasons', 'mass_parts', 'authors', 'tempo_text',
            'tempo', 'publish', 'url', )
