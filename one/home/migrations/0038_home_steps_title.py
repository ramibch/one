# Generated by Django 5.2 on 2025-04-07 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0037_stepaction_description_de_stepaction_description_en_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="home",
            name="steps_title",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
