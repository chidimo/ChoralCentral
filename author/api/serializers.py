from rest_framework import serializers
from ..models import Author
from siteuser.api.serializers import SiteUserSerializer

class AuthorSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    creator = SiteUserSerializer()
    class Meta:
        model = Author
        fields = ('creator', 'first_name', 'last_name', 'url')
