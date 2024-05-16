from django.conf import settings
from django.urls import reverse
from rest_framework import serializers

from links_handling.models import AddressUrl


class CreateShortUrlModelSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(
        max_length=32,
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = AddressUrl
        fields = [AddressUrl.Keys.original_url, AddressUrl.Keys.short_url]

    def to_representation(self, instance: AddressUrl) -> dict:
        instance_repr: dict = super().to_representation(instance)
        instance_repr["short_url"]: str = instance.get_full_short_url()
        return instance_repr


class RetrieveOriginalUrlModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressUrl
        fields = [AddressUrl.Keys.original_url]
