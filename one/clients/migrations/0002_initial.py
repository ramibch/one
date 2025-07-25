# Generated by Django 5.2 on 2025-06-15 18:44

import auto_prefetch
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("clients", "0001_initial"),
        ("sites", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="user",
            field=auto_prefetch.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="pathredirect",
            name="from_path",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="clients.path",
            ),
        ),
        migrations.AddField(
            model_name="pathredirect",
            name="sites",
            field=models.ManyToManyField(to="sites.site"),
        ),
        migrations.AddField(
            model_name="pathredirect",
            name="to_path",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="clients.path",
            ),
        ),
        migrations.AddField(
            model_name="request",
            name="client",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="clients.client"
            ),
        ),
        migrations.AddField(
            model_name="request",
            name="path",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="clients.path"
            ),
        ),
        migrations.AddField(
            model_name="request",
            name="site",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="sites.site"
            ),
        ),
        migrations.AddIndex(
            model_name="client",
            index=models.Index(
                condition=models.Q(("geoinfo__isnull", False)),
                fields=["geoinfo"],
                name="client_geoinfo_fkey",
            ),
        ),
    ]
