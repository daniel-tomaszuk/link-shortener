import string

from django.db import models

from link_shortener.settings import APP_BASE_URL


class AddressUrl(models.Model):
    SHORT_URL_ALLOWED_CHARS = string.digits + string.ascii_letters

    original_url = models.CharField(max_length=2048)
    short_url = models.CharField(max_length=32)

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
        short_url: str = self.__encode_base62()
        return APP_BASE_URL + short_url

    def get_original_url(self, short_url: str) -> str:
        # TODO - implement
        return ""

    def __encode_base62(self) -> str:
        """
        Uses python `hash()` function to product int hash of an original URL.
        Then produces shortened version using digits and ASCII letters (lower and uppercase).
        """
        original_url_hash: int = hash(self.original_url)
        if original_url_hash == 0:
            return self.SHORT_URL_ALLOWED_CHARS[0]

        short_url: list[str] = []
        original_url_hash: int = (
            original_url_hash if original_url_hash > 0 else -1 * original_url_hash
        )
        while original_url_hash:
            original_url_hash, div_remaining = divmod(
                original_url_hash, len(self.SHORT_URL_ALLOWED_CHARS)
            )
            short_url.append(self.SHORT_URL_ALLOWED_CHARS[div_remaining])
        return "".join(short_url)
