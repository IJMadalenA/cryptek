# Generated by Django 5.1.7 on 2025-04-01 12:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("blog_app", "0002_initial"),
        ("message_app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="messagesent",
            name="user_sender",
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="notification",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="socialshare",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="social_shares", to="blog_app.entry"
            ),
        ),
    ]
