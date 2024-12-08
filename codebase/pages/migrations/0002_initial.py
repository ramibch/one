# Generated by Django 5.1.3 on 2024-12-07 22:36

import auto_prefetch
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pages", "0001_initial"),
        ("sites", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pagessubmodule",
            name="sites",
            field=models.ManyToManyField(to="sites.site"),
        ),
        migrations.AddField(
            model_name="page",
            name="submodule",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="pages.pagessubmodule"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="page",
            unique_together={("folder", "subfolder")},
        ),
    ]