# Generated by Django 5.1.4 on 2025-02-22 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("etsy", "0044_remove_userlistingimage_name"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UserListingImage",
            new_name="ListingImage",
        ),
    ]
