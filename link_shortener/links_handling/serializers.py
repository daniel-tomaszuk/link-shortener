from links_handling.models import AddressUrl
from rest_framework import serializers


class CreateShortUrlModelSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(
        max_length=32,
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = AddressUrl
        fields = [AddressUrl.Keys.original_url, AddressUrl.Keys.short_url]
