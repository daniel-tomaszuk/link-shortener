# Generated by Django 5.0.6 on 2024-05-16 10:50

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("links_handling", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="addressurl",
            name="short_url",
            field=models.CharField(db_index=True, max_length=32, unique=True),
        ),
    ]
