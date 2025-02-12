# Generated by Django 5.1.6 on 2025-02-12 03:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library_tomb", "0002_comment_parent"),
    ]

    operations = [
        migrations.AddField(
            model_name="like",
            name="ip_address",
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AddField(
            model_name="like",
            name="type",
            field=models.CharField(
                choices=[("like", "Like"), ("dislike", "Dislike")],
                default="like",
                max_length=7,
            ),
        ),
        migrations.AddField(
            model_name="like",
            name="user_agent",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
