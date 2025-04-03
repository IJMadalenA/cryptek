# Generated by Django 5.1.7 on 2025-04-01 12:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("blog_app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="comments", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="entry",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="entries", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="entry",
            name="categories",
            field=models.ManyToManyField(blank=True, related_name="entries", to="blog_app.category"),
        ),
        migrations.AddField(
            model_name="comment",
            name="entry",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="blog_app.entry"
            ),
        ),
        migrations.AddField(
            model_name="entryanalytics",
            name="entry",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, related_name="analytics", to="blog_app.entry"
            ),
        ),
        migrations.AddField(
            model_name="entryreaction",
            name="entry",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="reactions", to="blog_app.entry"
            ),
        ),
        migrations.AddField(
            model_name="entryreaction",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="reactions", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="entryversion",
            name="entry",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="versions", to="blog_app.entry"
            ),
        ),
        migrations.AddField(
            model_name="like",
            name="entry",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="likes", to="blog_app.entry"
            ),
        ),
        migrations.AddField(
            model_name="like",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="likes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="multimedia",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="media", to="blog_app.entry"
            ),
        ),
        migrations.AddField(
            model_name="entry",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="entries", to="blog_app.tag"),
        ),
    ]
