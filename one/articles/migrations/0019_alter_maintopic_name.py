# Generated by Django 5.2 on 2025-04-14 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0018_rename_articleparentfolder_maintopic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="maintopic",
            name="name",
            field=models.CharField(editable=False, max_length=64, unique=True),
        ),
    ]
