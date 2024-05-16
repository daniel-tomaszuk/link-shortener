from django.db import models


class AddressUrl(models.Model):
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
        # TODO - implement
        return ""

    def get_original_url(self, short_url: str) -> str:
        # TODO - implement
        return ""
