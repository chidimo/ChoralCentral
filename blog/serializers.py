from rest_framework import serializers
from .models import Post
from siteuser.serializers import SiteUserSerializer

class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    creator = SiteUserSerializer()
    class Meta:
        model = Post
        fields = ('creator', 'title', 'subtitle', 'body', 'url', )
