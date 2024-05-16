import string
from datetime import datetime
from time import sleep

from django.conf import settings
from django.core.exceptions import BadRequest
from django.db import models
from django.http import HttpResponseBadRequest
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import APIException

from link_shortener.settings import APP_BASE_URL


class AddressUrl(models.Model):
    SHORT_URL_ALLOWED_CHARS = string.digits + string.ascii_letters
    MAX_RETRIES = 2

    original_url = models.CharField(max_length=2048)
    short_url = models.CharField(max_length=32, unique=True, db_index=True)

    class Keys:
        id = "id"
        original_url = "original_url"
        short_url = "short_url"

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ) -> None:
        # Save original url into the DB, create shortened version on save
        self.short_url: str = self.get_short_url()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def get_short_url(self) -> str:
        short_url: str = self.__get_unique_short_code()
        return short_url

    def get_full_short_url(self) -> str:
        return settings.APP_BASE_URL + reverse(
            "retrieve-original-url", args=(self.short_url,)
        )

    def __get_unique_short_code(self) -> str:
        counter = 0
        short_url: str = self.__hash_function()
        while counter < self.MAX_RETRIES:
            short_url_already_used: bool = AddressUrl.objects.filter(
                short_url=short_url
            ).exists()
            if not short_url_already_used:
                return short_url

            # encode once more to avoid duplicates
            short_url: str = self.__hash_function(raw_data=short_url)
            counter += 1

        # could not generate unique short code, raise Exception
        raise BadRequest()

    def __hash_function(self, raw_data: str | None = None) -> str:
        """
        Uses python `hash()` function to product int hash of an original URL.
        Then produces shortened version using digits and ASCII letters (lower and uppercase).
        """
        original_url_hash: int = hash(raw_data or self.original_url)
        if original_url_hash == 0:
            return self.SHORT_URL_ALLOWED_CHARS[0]

        short_url: list[str] = []
        original_url_hash: int = (
            original_url_hash if original_url_hash > 0 else -1 * original_url_hash
        )

        # use timestamps to randomize
        original_url_hash: int = original_url_hash // int(datetime.now().timestamp())
        while original_url_hash:
            original_url_hash, div_remaining = divmod(
                original_url_hash, len(self.SHORT_URL_ALLOWED_CHARS)
            )
            short_url.append(self.SHORT_URL_ALLOWED_CHARS[div_remaining])
        return "".join(short_url)
