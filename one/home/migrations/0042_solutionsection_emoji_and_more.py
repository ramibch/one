# Generated by Django 5.2 on 2025-04-19 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0041_problemsection_emoji"),
    ]

    operations = [
        migrations.AddField(
            model_name="solutionsection",
            name="emoji",
            field=models.CharField(db_default="💡", max_length=8),
        ),
        migrations.AlterField(
            model_name="problemsection",
            name="description",
            field=models.TextField(
                help_text="Reflect here the problem of the user. Use bullet list"
            ),
        ),
        migrations.AlterField(
            model_name="problemsection",
            name="description_de",
            field=models.TextField(
                help_text="Reflect here the problem of the user. Use bullet list",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="problemsection",
            name="description_en",
            field=models.TextField(
                help_text="Reflect here the problem of the user. Use bullet list",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="problemsection",
            name="description_es",
            field=models.TextField(
                help_text="Reflect here the problem of the user. Use bullet list",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="problemsection",
            name="description_fr",
            field=models.TextField(
                help_text="Reflect here the problem of the user. Use bullet list",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="problemsection",
            name="description_it",
            field=models.TextField(
                help_text="Reflect here the problem of the user. Use bullet list",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="problemsection",
            name="description_nl",
            field=models.TextField(
                help_text="Reflect here the problem of the user. Use bullet list",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="problemsection",
            name="description_pt",
            field=models.TextField(
                help_text="Reflect here the problem of the user. Use bullet list",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="solutionsection",
            name="description",
            field=models.TextField(
                help_text="Introduce our product/service as the solution."
            ),
        ),
        migrations.AlterField(
            model_name="solutionsection",
            name="description_de",
            field=models.TextField(
                help_text="Introduce our product/service as the solution.", null=True
            ),
        ),
        migrations.AlterField(
            model_name="solutionsection",
            name="description_en",
            field=models.TextField(
                help_text="Introduce our product/service as the solution.", null=True
            ),
        ),
        migrations.AlterField(
            model_name="solutionsection",
            name="description_es",
            field=models.TextField(
                help_text="Introduce our product/service as the solution.", null=True
            ),
        ),
        migrations.AlterField(
            model_name="solutionsection",
            name="description_fr",
            field=models.TextField(
                help_text="Introduce our product/service as the solution.", null=True
            ),
        ),
        migrations.AlterField(
            model_name="solutionsection",
            name="description_it",
            field=models.TextField(
                help_text="Introduce our product/service as the solution.", null=True
            ),
        ),
        migrations.AlterField(
            model_name="solutionsection",
            name="description_nl",
            field=models.TextField(
                help_text="Introduce our product/service as the solution.", null=True
            ),
        ),
        migrations.AlterField(
            model_name="solutionsection",
            name="description_pt",
            field=models.TextField(
                help_text="Introduce our product/service as the solution.", null=True
            ),
        ),
    ]
