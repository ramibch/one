# Generated by Django 5.2 on 2025-05-10 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0003_rename_jobs_url_company_jobs_page_url_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="jobs_container_class",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name="company",
            name="jobs_container_tag",
            field=models.CharField(default="div"),
        ),
        migrations.AlterField(
            model_name="company",
            name="job_link_class",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
