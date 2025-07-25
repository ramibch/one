# Generated by Django 5.2 on 2025-06-15 18:44

import auto_prefetch
import django.db.models.deletion
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("base", "0002_initial"),
        ("clients", "0001_initial"),
        ("products", "0001_initial"),
        ("sites", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="link",
            name="product",
            field=auto_prefetch.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="products.product",
            ),
        ),
        migrations.AddField(
            model_name="searchterm",
            name="client",
            field=auto_prefetch.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="clients.client",
            ),
        ),
        migrations.AddField(
            model_name="searchterm",
            name="site",
            field=auto_prefetch.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="sites.site"
            ),
        ),
    ]
