import string

import pytest
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from links_handling.models import AddressUrl


class BaseTestCase:
    @staticmethod
    def get_create_body() -> dict:
        return {"original_url": "https://example.com/test-1/test-2/test-3"}


@pytest.mark.django_db
class TestShortUrlCreate(BaseTestCase):

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

    @freeze_time("2024-05-16")
    @pytest.mark.parametrize(
        "original_url, original_url_hash, expected_short_url",
        [
            (
                "http://example.com/very-very/long/url/even-longer",
                6108607072535043855,
                "http://localhost:8000/dz7WS3",
            ),
            (
                "http://example.com/text?param-1=abc&param-2=12xyz9",
                7579468129359924641,
                "http://localhost:8000/sSZWO4",
            ),
            (
                "https://wikipedia.org",
                1786732465404246247,
                "http://localhost:8000/kwjt81",
            ),
        ],
    )
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
        assert link_object.get_full_short_url() == expected_short_url

    def test_short_url_allowed_chars(self):
        assert len(AddressUrl.SHORT_URL_ALLOWED_CHARS) == len(
            string.digits + string.ascii_letters
        )
        assert sorted(AddressUrl.SHORT_URL_ALLOWED_CHARS) == sorted(
            string.digits + string.ascii_letters
        )

    def test_create_shortened_url__missing_original_url_in_payload(self, client):
        # When payload is empty
        url = reverse("create-short-url")
        response = client.post(url, data={})

        # Then response as expected
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_shortened_url__original_url_as_empty_string(self, client):
        # When original URL given as empty string
        url = reverse("create-short-url")
        response = client.post(url, data={"original_url": ""})

        # Then response as expected
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_shortened_url__duplicates__are_retried(self, client):
        # Given payload is correct
        data: dict = self.get_create_body()

        # and URL as expected
        url: str = reverse("create-short-url")

        # When client posts new shortened URL with proper payload
        response = client.post(url, data=data)

        # Then response as expected
        assert response.status_code == status.HTTP_201_CREATED

        # When client posts the same URL once more
        response = client.post(url, data=data)

        # Then there is no error
        assert response.status_code == status.HTTP_201_CREATED

        # and link is created in the DB with different short code
        assert AddressUrl.objects.filter(original_url=data["original_url"]).count() == 2

        # and new short code saved in the DB as expected
        short_code = response.data["short_url"].split("/")[-1]
        assert AddressUrl.objects.filter(short_url=short_code).count() == 1

    def test_create_shortened_url__duplicates__error_rised_if_retried_to_many_times(
        self, client, monkeypatch
    ):

        # Given hash function could not generate unique short code
        def mock_hash_function(*args, **kwargs) -> str:
            return "12345"

        monkeypatch.setattr(
            AddressUrl, "_AddressUrl__hash_function", mock_hash_function
        )

        # and payload is correct
        data: dict = self.get_create_body()

        # and URL as expected
        url: str = reverse("create-short-url")

        # When client posts new shortened URL with proper payload
        response = client.post(url, data=data)

        # Then response as expected and DB object created - no duplicates so far
        assert response.status_code == status.HTTP_201_CREATED
        assert AddressUrl.objects.filter(original_url=data["original_url"]).count() == 1

        # When client posts the same URL once more,
        # so duplicates would be created and hash function can not create new unique code
        response = client.post(url, data=data)

        # Then there is an error and new link is not created in the DB
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert AddressUrl.objects.filter(original_url=data["original_url"]).count() == 1


@pytest.mark.django_db
class TestOriginalUrlRetrieve(BaseTestCase):

    def test_get_original_link__does_not_exist(self, client):
        url = reverse("retrieve-original-url", args=("dummy-short-url",))
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_original__link_does_exist(self, client):
        # Given original URL is passed to create short version
        original_url = "https://example.com/very-long-link-with-a-lot-of-query-params"
        post_url = reverse("create-short-url")
        response = client.post(post_url, data=dict(original_url=original_url))
        assert response.status_code == status.HTTP_201_CREATED

        short_url_code = AddressUrl.objects.get(original_url=original_url).short_url

        # When getting the original link using the short version
        get_url = reverse("retrieve-original-url", args=(short_url_code,))
        response = client.get(get_url)

        # Then response as expected and original url is correct
        assert response.status_code == status.HTTP_200_OK
        assert response.data["original_url"] == original_url
