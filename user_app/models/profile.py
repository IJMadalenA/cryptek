from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from PIL import Image
from user_app.models.cryptek_user import CryptekUser


class Profile(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = "public", _("Public")
        PRIVATE = "private", _("Private")

    user = models.OneToOneField(CryptekUser, on_delete=models.CASCADE, related_name="profile", editable=False)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    location = models.CharField(max_length=120, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    social_links = models.JSONField(default=dict, blank=True)  # Stores social networks in JSON format.
    visibility = models.CharField(max_length=10, choices=Visibility.choices, default=Visibility.PUBLIC)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Optimizes and resizes the image before saving it."""
        if self.profile_picture:
            img = Image.open(self.profile_picture)
            output_size = (400, 400)

            # Convert to RGB if necessary (avoids errors with PNGs and WebP).
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Resize image while maintaining aspect ratio.
            img.thumbnail(output_size)

            # Save in WebP format for better compression
            output = BytesIO()
            img.save(output, format="WEBP", quality=85)
            output.seek(0)

            # Replace original image with optimized image.
            self.profile_picture = ContentFile(output.read(), name=f"{self.user.username}.webp")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def get_profile_picture(self):
        return self.profile_picture.url if self.profile_picture else "/static/default-cover.jpg"

    def get_bio(self):
        return self.bio or ""

    def is_complete(self):
        """Returns True if the profile is completely filled."""
        return all([self.bio, self.profile_picture, self.location, self.birth_date, self.website, self.phone_number])

    def get_social_links(self):
        """Returns social network links as a dictionary."""
        return self.social_links or {}


@receiver(pre_save, sender=Profile)
def delete_old_profile_picture(sender, instance, **kwargs):
    """Deletes the previous image when a new one is uploaded."""
    if instance.pk:
        try:
            old_profile = Profile.objects.get(pk=instance.pk)
            if old_profile.profile_picture and old_profile.profile_picture != instance.profile_picture:
                old_profile.profile_picture.delete(save=False)
        except Profile.DoesNotExist:
            pass
