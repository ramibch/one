# Generated by Django 5.0.4 on 2024-04-28 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emails", "0007_alter_pastrecipient_addresses_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="pastrecipient",
            name="var1",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="pastrecipient",
            name="var2",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="pastrecipient",
            name="var3",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="pastrecipient",
            name="var4",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="pastrecipient",
            name="var5",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]