from rest_framework.generics import CreateAPIView

from links_handling.models import AddressUrl
from links_handling.serializers import CreateShortUrlModelSerializer


class ShortUrlCreateAPIView(CreateAPIView):
    queryset = AddressUrl.objects.all()
    serializer_class = CreateShortUrlModelSerializer
