# Generated by Django 5.1.4 on 2024-12-21 07:34

import auto_prefetch
import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("articles", "0004_rename_folder_article_folder_name_and_more"),
        ("faqs", "0003_remove_faq_can_be_shown_in_home"),
        ("links", "0002_initial"),
        ("sites", "0005_site_brand_name_alter_site_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Home",
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
                ("allow_translation", models.BooleanField(default=False)),
                ("override_translated_fields", models.BooleanField(default=False)),
                ("title", models.CharField(default="", max_length=64)),
                ("title_en", models.CharField(default="", max_length=64, null=True)),
                ("title_de", models.CharField(default="", max_length=64, null=True)),
                ("title_es", models.CharField(default="", max_length=64, null=True)),
                ("title_fr", models.CharField(default="", max_length=64, null=True)),
                ("title_el", models.CharField(default="", max_length=64, null=True)),
                ("title_it", models.CharField(default="", max_length=64, null=True)),
                ("title_nl", models.CharField(default="", max_length=64, null=True)),
                ("title_pl", models.CharField(default="", max_length=64, null=True)),
                ("title_pt", models.CharField(default="", max_length=64, null=True)),
                ("title_ru", models.CharField(default="", max_length=64, null=True)),
                ("title_sk", models.CharField(default="", max_length=64, null=True)),
                ("title_sl", models.CharField(default="", max_length=64, null=True)),
                ("title_sv", models.CharField(default="", max_length=64, null=True)),
                ("title_tr", models.CharField(default="", max_length=64, null=True)),
                ("title_uk", models.CharField(default="", max_length=64, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("enable_section_changing", models.BooleanField(default=False)),
                ("display_last_articles", models.BooleanField(default=False)),
                ("num_articles", models.PositiveSmallIntegerField(default=6)),
                ("display_faqs", models.BooleanField(default=False)),
                (
                    "benefits_title",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("steps_title", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "site",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="sites.site"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            # bases=(models.Model, one.base.utils.mixins.PageMixin),
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="HeroSection",
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
                ("allow_translation", models.BooleanField(default=False)),
                ("override_translated_fields", models.BooleanField(default=False)),
                ("headline", models.TextField(max_length=256)),
                ("headline_en", models.TextField(max_length=256, null=True)),
                ("headline_de", models.TextField(max_length=256, null=True)),
                ("headline_es", models.TextField(max_length=256, null=True)),
                ("headline_fr", models.TextField(max_length=256, null=True)),
                ("headline_el", models.TextField(max_length=256, null=True)),
                ("headline_it", models.TextField(max_length=256, null=True)),
                ("headline_nl", models.TextField(max_length=256, null=True)),
                ("headline_pl", models.TextField(max_length=256, null=True)),
                ("headline_pt", models.TextField(max_length=256, null=True)),
                ("headline_ru", models.TextField(max_length=256, null=True)),
                ("headline_sk", models.TextField(max_length=256, null=True)),
                ("headline_sl", models.TextField(max_length=256, null=True)),
                ("headline_sv", models.TextField(max_length=256, null=True)),
                ("headline_tr", models.TextField(max_length=256, null=True)),
                ("headline_uk", models.TextField(max_length=256, null=True)),
                ("subheadline", models.TextField(max_length=256)),
                ("subheadline_en", models.TextField(max_length=256, null=True)),
                ("subheadline_de", models.TextField(max_length=256, null=True)),
                ("subheadline_es", models.TextField(max_length=256, null=True)),
                ("subheadline_fr", models.TextField(max_length=256, null=True)),
                ("subheadline_el", models.TextField(max_length=256, null=True)),
                ("subheadline_it", models.TextField(max_length=256, null=True)),
                ("subheadline_nl", models.TextField(max_length=256, null=True)),
                ("subheadline_pl", models.TextField(max_length=256, null=True)),
                ("subheadline_pt", models.TextField(max_length=256, null=True)),
                ("subheadline_ru", models.TextField(max_length=256, null=True)),
                ("subheadline_sk", models.TextField(max_length=256, null=True)),
                ("subheadline_sl", models.TextField(max_length=256, null=True)),
                ("subheadline_sv", models.TextField(max_length=256, null=True)),
                ("subheadline_tr", models.TextField(max_length=256, null=True)),
                ("subheadline_uk", models.TextField(max_length=256, null=True)),
                ("cta_title", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "cta_title_en",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_de",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_es",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_fr",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_el",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_it",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_nl",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_pl",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_pt",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_ru",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_sk",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_sl",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_sv",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_tr",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "cta_title_uk",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("cta_new_tab", models.BooleanField(default=False)),
                ("image", models.ImageField(upload_to="homepages/hero/")),
                ("is_active", models.BooleanField()),
                (
                    "cta_link",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="links.link"
                    ),
                ),
                (
                    "home",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="home.home"
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
        migrations.CreateModel(
            name="FAQsSection",
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
                ("allow_translation", models.BooleanField(default=False)),
                ("override_translated_fields", models.BooleanField(default=False)),
                ("title", models.CharField(max_length=64)),
                ("title_en", models.CharField(max_length=64, null=True)),
                ("title_de", models.CharField(max_length=64, null=True)),
                ("title_es", models.CharField(max_length=64, null=True)),
                ("title_fr", models.CharField(max_length=64, null=True)),
                ("title_el", models.CharField(max_length=64, null=True)),
                ("title_it", models.CharField(max_length=64, null=True)),
                ("title_nl", models.CharField(max_length=64, null=True)),
                ("title_pl", models.CharField(max_length=64, null=True)),
                ("title_pt", models.CharField(max_length=64, null=True)),
                ("title_ru", models.CharField(max_length=64, null=True)),
                ("title_sk", models.CharField(max_length=64, null=True)),
                ("title_sl", models.CharField(max_length=64, null=True)),
                ("title_sv", models.CharField(max_length=64, null=True)),
                ("title_tr", models.CharField(max_length=64, null=True)),
                ("title_uk", models.CharField(max_length=64, null=True)),
                (
                    "faqs",
                    models.ManyToManyField(
                        limit_choices_to={"is_active": True}, to="faqs.faq"
                    ),
                ),
                (
                    "home",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="home.home"
                    ),
                ),
            ],
            options={
                "verbose_name": "FAQs Section",
                "verbose_name_plural": "FAQs Sections",
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="BenefitsSection",
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
                ("allow_translation", models.BooleanField(default=False)),
                ("override_translated_fields", models.BooleanField(default=False)),
                ("emoji", models.CharField(max_length=8)),
                ("is_active", models.BooleanField()),
                (
                    "home",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="home.home"
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
        migrations.CreateModel(
            name="ArticlesSection",
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
                ("allow_translation", models.BooleanField(default=False)),
                ("override_translated_fields", models.BooleanField(default=False)),
                ("title", models.CharField(max_length=64)),
                ("auto_add_articles", models.BooleanField(default=False)),
                ("articles", models.ManyToManyField(to="articles.article")),
                (
                    "home",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="home.home"
                    ),
                ),
            ],
            options={
                "verbose_name": "Articles Section",
                "verbose_name_plural": "Articles Sections",
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="ProblemSection",
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
                ("title", models.CharField(max_length=64)),
                ("description", models.TextField()),
                ("is_active", models.BooleanField()),
                (
                    "home",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="home.home"
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
        migrations.CreateModel(
            name="SolutionSection",
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
                ("allow_translation", models.BooleanField(default=False)),
                ("override_translated_fields", models.BooleanField(default=False)),
                ("title", models.CharField(max_length=64)),
                ("description", models.TextField()),
                ("is_active", models.BooleanField()),
                (
                    "home",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="home.home"
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
        migrations.CreateModel(
            name="StepAction",
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
                ("allow_translation", models.BooleanField(default=False)),
                ("override_translated_fields", models.BooleanField(default=False)),
                ("step_label", models.CharField(default="01", max_length=4)),
                ("title", models.CharField(max_length=64)),
                ("description", models.TextField()),
                ("is_active", models.BooleanField()),
                (
                    "home",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.home"
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
        migrations.CreateModel(
            name="UserHome",
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
                ("allow_translation", models.BooleanField(default=False)),
                ("override_translated_fields", models.BooleanField(default=False)),
                (
                    "site",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="sites.site"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            # bases=(models.Model, one.base.utils.mixins.PageMixin),
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
    ]
