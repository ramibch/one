# Generated by Django 5.1.4 on 2024-12-21 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("faqs", "0003_remove_faq_can_be_shown_in_home"),
    ]

    operations = [
        migrations.AddField(
            model_name="faq",
            name="featured",
            field=models.BooleanField(default=False),
        ),
    ]
