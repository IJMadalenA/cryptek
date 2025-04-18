# Generated by Django 5.1.7 on 2025-04-08 09:37

import django.db.models.deletion
import markdownx.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("subtitle", models.CharField(max_length=250)),
                ("description", models.TextField(blank=True)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("thumbnail", models.ImageField(blank=True, null=True, upload_to="category_thumbnails/")),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Entry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100)),
                ("content", markdownx.models.MarkdownxField()),
                ("overview", models.TextField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("status", models.IntegerField(choices=[(0, "Draft"), (1, "Published"), (2, "hidden")], default=0)),
                ("featured", models.BooleanField(default=False)),
                ("publish_date", models.DateTimeField(blank=True, default=None, null=True)),
                ("header_image", models.ImageField(blank=True, null=True, upload_to="header_images/")),
                ("cdn_image_url", models.URLField(blank=True, null=True, unique=True)),
                ("cdn_image_public_id", models.CharField(blank=True, max_length=200, null=True)),
                ("slug", models.SlugField(blank=True, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("categories", models.ManyToManyField(related_name="entries", to="blog_app.category")),
                ("tags", models.ManyToManyField(blank=True, related_name="entries", to="blog_app.tag")),
            ],
            options={
                "verbose_name_plural": "Entries",
                "ordering": ["-created_at"],
                "get_latest_by": "created_at",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="blog_app.comment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "entry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="blog_app.entry"
                    ),
                ),
            ],
            options={
                "ordering": ("created_at",),
            },
        ),
        migrations.CreateModel(
            name="EntryAnalytics",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("views", models.IntegerField(default=0)),
                ("read_time", models.IntegerField(default=0)),
                (
                    "entry",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name="analytics", to="blog_app.entry"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EntryReaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reaction", models.CharField(max_length=50)),
                (
                    "entry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="reactions", to="blog_app.entry"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reactions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EntryVersion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField()),
                ("version_date", models.DateTimeField(auto_now_add=True)),
                (
                    "entry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="versions", to="blog_app.entry"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "type",
                    models.CharField(choices=[("like", "Like"), ("dislike", "Dislike")], default="like", max_length=7),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user_agent", models.CharField(blank=True, max_length=255, null=True)),
                ("ip_address", models.CharField(blank=True, max_length=45, null=True)),
                (
                    "entry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="likes", to="blog_app.entry"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="likes", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Multimedia",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="media/")),
                ("media_type", models.CharField(max_length=50)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="media", to="blog_app.entry"
                    ),
                ),
            ],
        ),
    ]
