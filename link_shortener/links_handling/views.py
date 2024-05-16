from django.shortcuts import render
from links_handling.models import AddressUrl
from links_handling.serializers import CreateShortUrlModelSerializer
from rest_framework.generics import CreateAPIView


class ShortUrlCreateAPIView(CreateAPIView):
    queryset = AddressUrl.objects.all()
    serializer_class = CreateShortUrlModelSerializer
