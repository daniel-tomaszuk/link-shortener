import string

import pytest
from django.urls import reverse
from rest_framework import status

from links_handling.models import AddressUrl


class BaseTestCase:
    @staticmethod
    def get_create_body() -> dict:
        return {"original_url": "https://example.com/test-1/test-2/test-3"}


class TestShortUrlCreate(BaseTestCase):

    @pytest.mark.django_db
    def test_create_shortened_url__success(self, client):
        # Given payload is correct
        data: dict = self.get_create_body()

        # and URL as expected
        url: str = reverse("create-short-url")

        # When client posts new shortened URL with proper payload
        response = client.post(url, data=data)

        # Then response as expected
        assert response.status_code == status.HTTP_201_CREATED
        # and object created in the DB
        assert AddressUrl.objects.filter(original_url=data["original_url"]).exists()

    @pytest.mark.parametrize(
        "original_url, original_url_hash, expected_short_url",
        [
            (
                "http://example.com/very-very/long/url/even-longer",
                6108607072535043855,
                "http://localhost:8000/R1n0I65ufh7",
            ),
            (
                "http://example.com/text?param-1=abc&param-2=12xyz9",
                7579468129359924641,
                "http://localhost:8000/nfgxrQK2U19",
            ),
            (
                "https://wikipedia.org",
                1786732465404246247,
                "http://localhost:8000/Nnfph1JfZ72",
            ),
        ],
    )
    @pytest.mark.django_db
    def test_create_shortened_url__success__short_url_value(
        self, client, monkeypatch, original_url, original_url_hash, expected_short_url
    ):
        # Given payload is correct
        data: dict = self.get_create_body()
        data["original_url"] = original_url

        # and URL as expected
        url: str = reverse("create-short-url")

        # and hash function is mocked, so it returns expected value every time (for tests)
        monkeypatch.setattr("builtins.hash", lambda x: original_url_hash)

        # When client posts new shortened URL with proper payload
        response = client.post(url, data=data)

        # Then response code as expected
        assert response.status_code == status.HTTP_201_CREATED

        # and short url as expected
        link_object = AddressUrl.objects.get(original_url=data["original_url"])
        assert link_object.short_url == expected_short_url

    def test_short_url_allowed_chars(self):
        assert len(AddressUrl.SHORT_URL_ALLOWED_CHARS) == len(
            string.digits + string.ascii_letters
        )
        assert sorted(AddressUrl.SHORT_URL_ALLOWED_CHARS) == sorted(
            string.digits + string.ascii_letters
        )

    @pytest.mark.django_db
    def test_create_shortened_url__missing_original_url_in_payload(self, client):
        # When payload is empty
        url = reverse("create-short-url")
        response = client.post(url, data={})

        # Then response as expected
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_create_shortened_url__original_url_as_empty_string(self, client):
        # When original URL given as empty string
        url = reverse("create-short-url")
        response = client.post(url, data={"original_url": ""})

        # Then response as expected
        assert response.status_code == status.HTTP_400_BAD_REQUEST
