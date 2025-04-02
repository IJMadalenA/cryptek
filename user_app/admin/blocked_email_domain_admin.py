from django.contrib import admin

from user_app.models.blocked_email_domain import BlockedEmailDomain, BlockedEmailDomainExtension


@admin.register(BlockedEmailDomainExtension)
class BlockedEmailDomainExtensionAdmin(admin.ModelAdmin):
    list_display = ("domain_extension", "added_at")
    search_fields = ("domain_extension",)
    ordering = ("-added_at",)


@admin.register(BlockedEmailDomain)
class BlockedEmailDomainAdmin(admin.ModelAdmin):
    list_display = ("username", "domain", "domain_extension", "added_at", "is_blocked")
    list_filter = ("is_blocked", "domain_extension")
    search_fields = ("username", "domain")
    ordering = ("-added_at",)
    readonly_fields = ("added_at",)
