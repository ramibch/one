# Generated by Django 5.1.3 on 2024-12-09 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0004_topic"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="name_de",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_el",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_en",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_eo",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_es",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_fi",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_fr",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_it",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_nl",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_nn",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_pl",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_pt",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_pt_br",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_ru",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_sk",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_sl",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_sq",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_sr",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_sv",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_tr",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="name_uk",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_de",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_el",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_en",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_eo",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_es",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_fi",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_fr",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_it",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_nl",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_nn",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_pl",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_pt",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_pt_br",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_ru",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_sk",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_sl",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_sq",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_sr",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_sv",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_tr",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="slug_uk",
            field=models.SlugField(max_length=32, null=True, unique=True),
        ),
    ]