import pytest
from django.urls import reverse
from links_handling.models import AddressUrl
from rest_framework import status


class BaseTestCase:
    @staticmethod
    def get_create_body() -> dict:
        return {"original_url": "https://example.com/test-1/test-2/test-3"}


class TestShortUrlCreate(BaseTestCase):

    @pytest.mark.django_db
    def test_create_shortened_url__success(self, client):
        url = reverse("create-short-url")
        response = client.post(url, data=self.get_create_body())
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_create_shortened_url__missing_original_url_in_payload(self, client):
        url = reverse("create-short-url")
        response = client.post(url, data={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_create_shortened_url__original_url_as_empty_string(self, client):
        url = reverse("create-short-url")
        response = client.post(url, data={"original_url": ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
