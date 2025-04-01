from django.contrib import admin

from conscious_element.models.blocked_email_domain import BlockedEmailDomain


@admin.register(BlockedEmailDomain)
class BlockedEmailDomainAdmin(admin.ModelAdmin):
    list_display = ("domain", "added_at")
    search_fields = ("domain",)
