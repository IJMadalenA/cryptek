import os

from django.db import migrations


def add_social_applications(apps, schema_editor):
    SocialApp = apps.get_model("socialaccount", "SocialApp")
    Site = apps.get_model("sites", "Site")

    # Ensure the default site exists
    site, _ = Site.objects.get_or_create(id=1, defaults={"domain": "example.com", "name": "example.com"})

    default_social_apps = [
        {
            "provider": "github",
            "name": "GitHub",
            "client_id": os.environ.get("GITHUB_CLIENT_ID"),
            "secret": os.environ.get("GITHUB_CLIENT_SECRET"),
        },
        {
            "provider": "digitalocean",
            "name": "Digital Ocean",
            "client_id": os.environ.get("DIGITAL_OCEAN_CLIEN_ID"),
            "secret": os.environ.get("DIGITAL_OCEAN_CLIENT_SECRET"),
        },
        {
            "provider": "google",
            "name": "Google",
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
        },
        {
            "provider": "linkedin_oauth2",
            "name": "LinkedIn",
            "client_id": os.environ.get("LINKEDIN_CLIENT_ID"),
            "secret": os.environ.get("LINKEDIN_CLIENT_SECRET"),
        },
    ]

    for app_data in default_social_apps:
        if not SocialApp.objects.filter(provider=app_data["provider"]).exists():
            social_app = SocialApp.objects.create(
                provider=app_data["provider"],
                name=app_data["name"],
                client_id=app_data["client_id"],
                secret=app_data["secret"],
            )
            social_app.sites.set([site])  # Assign the site using the set() method


def remove_social_applications(apps, schema_editor):
    SocialApp = apps.get_model("socialaccount", "SocialApp")

    providers = ["github", "digitalocean", "google", "linkedin_oauth2"]

    SocialApp.objects.filter(provider__in=providers).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("user_app", "0004_alter_profile_user"),
        ("sites", "0002_alter_domain_unique"),  # Ensure the sites app migration is included
    ]

    operations = [
        migrations.RunPython(add_social_applications, remove_social_applications),
    ]
