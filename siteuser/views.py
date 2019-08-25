from collections import OrderedDict

from django.http import JsonResponse, HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response

from .models import CustomUser, SiteUser
from .serializers import CustomUserSerializer, SiteUserSerializer, RolesSerializer

class SiteUserViewSet(viewsets.ModelViewSet):
    queryset = SiteUser.objects.all()
    serializer_class = SiteUserSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})


    def create(self, request):
        if request.method == 'POST':
            data = request.data
            name = data['name']

            try:
                Version.objects.get(name=name)
                return JsonResponse(f'{name} version already exists.', status=400, safe=False)
            except:
                version, created = Version.objects.get_or_create(name=name)
                return JsonResponse(f'{name} version created.', status=201, safe=False)     

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})
