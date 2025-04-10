# Generated by Django 5.2 on 2025-04-07 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0036_remove_benefititem_section_benefititem_home_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stepaction",
            name="description_de",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="description_en",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="description_es",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="description_fr",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="description_it",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="description_nl",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="description_pt",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="title_de",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="title_en",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="title_es",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="title_fr",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="title_it",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="title_nl",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="stepaction",
            name="title_pt",
            field=models.CharField(max_length=64, null=True),
        ),
    ]
