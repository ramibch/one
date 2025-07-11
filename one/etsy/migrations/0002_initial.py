# Generated by Django 5.2 on 2025-06-15 18:44

import auto_prefetch
import django.db.models.deletion
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("etsy", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="etsyauth",
            name="user",
            field=auto_prefetch.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="listing",
            name="etsy_auth",
            field=auto_prefetch.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="etsy.etsyauth",
            ),
        ),
        migrations.AddField(
            model_name="listingfile",
            name="listing",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="files",
                to="etsy.listing",
            ),
        ),
        migrations.AddField(
            model_name="listingimage",
            name="listing",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="etsy.listing",
            ),
        ),
        migrations.AddField(
            model_name="shop",
            name="etsy_auth",
            field=auto_prefetch.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="etsy.etsyauth"
            ),
        ),
    ]
