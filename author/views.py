from collections import OrderedDict

from django.http import JsonResponse, HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Author
from .serializers import AuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})
