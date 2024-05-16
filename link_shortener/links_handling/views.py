from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView

from links_handling.models import AddressUrl
from links_handling.serializers import CreateShortUrlModelSerializer
from links_handling.serializers import RetrieveOriginalUrlModelSerializer


class ShortUrlCreateAPIView(CreateAPIView):
    queryset = AddressUrl.objects.all()
    serializer_class = CreateShortUrlModelSerializer


class OriginalUrlRetrieveAPIView(RetrieveAPIView):
    queryset = AddressUrl.objects.all()
    serializer_class = RetrieveOriginalUrlModelSerializer
    lookup_field = "short_url"
