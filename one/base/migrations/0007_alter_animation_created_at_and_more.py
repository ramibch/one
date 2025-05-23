# Generated by Django 5.2 on 2025-05-23 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0006_alter_animation_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="animation",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="animation",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="contactmessage",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="searchterm",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
