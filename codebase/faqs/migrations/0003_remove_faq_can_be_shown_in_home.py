# Generated by Django 5.1.4 on 2024-12-20 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("faqs", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="faq",
            name="can_be_shown_in_home",
        ),
    ]