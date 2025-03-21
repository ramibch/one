# Generated by Django 5.1.4 on 2025-02-04 07:11

import auto_prefetch
import django.core.validators
import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models

import one.base.utils.db
import one.etsy.models


class Migration(migrations.Migration):

    dependencies = [
        ("etsy", "0016_shop_etsy_payload"),
        ("products", "0010_rename_summary_product_description_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserShop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.RenameModel(
            old_name="Listing",
            new_name="ProductListing",
        ),
        migrations.CreateModel(
            name="UserListing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.PositiveSmallIntegerField(
                        default=999,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(999),
                        ],
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Title can contain only letters, numbers, punctuation, mathematical symbols, whitespace, ™, ©, and ®. '%', ':', '&', and '+' can be used only once each.",
                        max_length=255,
                    ),
                ),
                ("description", models.TextField()),
                ("price", models.FloatField()),
                (
                    "who_made",
                    models.CharField(
                        choices=[
                            ("i_did", "I did"),
                            ("someone_else", "Someone else"),
                            ("collective", "Collective"),
                        ],
                        default="i_did",
                        max_length=32,
                    ),
                ),
                (
                    "when_made",
                    models.CharField(
                        choices=[
                            ("made_to_order", "Made to order"),
                            ("2020_2025", "2020 - 2025"),
                            ("2010_2019", "2010 - 2019"),
                            ("2006_2009", "2006 - 2009"),
                            ("before_2006", "Before 2006"),
                        ],
                        default="2020_2025",
                        max_length=32,
                    ),
                ),
                (
                    "taxonomy_id",
                    models.PositiveIntegerField(
                        choices=[(2078, "Digital prints")], default=2078
                    ),
                ),
                ("shop_section_id", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "tags",
                    one.base.utils.db.ChoiceArrayField(
                        base_field=models.CharField(max_length=20), size=13
                    ),
                ),
                (
                    "is_personalizable",
                    models.BooleanField(
                        blank=True,
                        help_text="This listing is personalizable or not.",
                        null=True,
                    ),
                ),
                (
                    "personalization_is_required",
                    models.BooleanField(
                        blank=True,
                        help_text="Listing requires personalization or not. Will only change if is_personalizable is 'true'.",
                        null=True,
                    ),
                ),
                (
                    "personalization_char_count_max",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        help_text="It represents the maximum length for the personalization message entered by the buyer. Will only change if is_personalizable is 'true'.",
                        null=True,
                    ),
                ),
                (
                    "personalization_instructions",
                    models.TextField(
                        blank=True,
                        help_text="It represents  instructions for the buyer to enter the personalization. Will only change if is_personalizable is 'true'.",
                        null=True,
                    ),
                ),
                (
                    "is_customizable",
                    models.BooleanField(
                        blank=True,
                        help_text="When true, a buyer may contact the seller for a customized order. The default value is true when a shop accepts custom orders. Does not apply to shops that do not accept custom orders.",
                        null=True,
                    ),
                ),
                (
                    "should_auto_renew",
                    models.BooleanField(
                        blank=True,
                        default=False,
                        help_text="Renews or not a listing for four months upon expiration.",
                        null=True,
                    ),
                ),
                (
                    "is_taxable",
                    models.BooleanField(
                        blank=True,
                        default=False,
                        help_text="Tax rates apply or not to this listing at checkout.",
                        null=True,
                    ),
                ),
                (
                    "listing_type",
                    models.CharField(
                        choices=[
                            ("physical", "Physical"),
                            ("download", "Download"),
                            ("both", "Both"),
                        ],
                        default="download",
                        help_text="An enumerated type string that indicates whether the listing is physical or a digital download.",
                        max_length=32,
                    ),
                ),
                ("state", models.CharField(max_length=32, null=True)),
                ("creation_timestamp", models.PositiveBigIntegerField(null=True)),
                ("created_timestamp", models.PositiveBigIntegerField(null=True)),
                ("ending_timestamp", models.PositiveBigIntegerField(null=True)),
                (
                    "original_creation_timestamp",
                    models.PositiveBigIntegerField(null=True),
                ),
                ("last_modified_timestamp", models.PositiveBigIntegerField(null=True)),
                ("updated_timestamp", models.PositiveBigIntegerField(null=True)),
                ("state_timestamp", models.PositiveBigIntegerField(null=True)),
                ("featured_rank", models.PositiveIntegerField(null=True)),
                ("url", models.URLField(null=True)),
                ("num_favorers", models.PositiveIntegerField(null=True)),
                ("non_taxable", models.BooleanField(null=True)),
                ("is_private", models.BooleanField(null=True)),
                ("language", models.CharField(max_length=32, null=True)),
                (
                    "user_shop_auth",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="etsy.usershopauth",
                    ),
                ),
                (
                    "user_shop",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="etsy.usershop"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
    ]
