# Generated by Django 5.1.4 on 2025-02-16 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("etsy", "0025_remove_userlisting_user_shop_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userlistingfile",
            name="name",
        ),
    ]
