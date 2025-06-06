from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from user_app.models.session import Session
from user_app.templatetags.session_filters import device, location


class ExpiredFilter(admin.SimpleListFilter):
    title = _("Is Valid")
    parameter_name = "active"

    def lookups(self, request, model_admin):
        return (("1", _("Active")), ("0", _("Expired")))

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(expire_date__gt=now())
        elif self.value() == "0":
            return queryset.filter(expire_date__lte=now())


class OwnerFilter(admin.SimpleListFilter):
    title = _("Owner")
    parameter_name = "owner"

    def lookups(self, request, model_admin):
        return (("my", _("Self")),)

    def queryset(self, request, queryset):
        if self.value() == "my":
            return queryset.filter(user=request.user)


class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "ip",
        "user",
        "is_valid",
        "location",
        "device",
    )
    fields = (
        ("user", "ip"),
        "user_agent",
        ("referer", "request_path"),
        "accept_language",
        "session_data",
        ("expire_date", "timestamp"),
    )
    search_fields = ()
    list_filter = ExpiredFilter, OwnerFilter
    exclude = ("session_key",)
    readonly_fields = (
        "user",
        "ip",
        "user_agent",
        "referer",
        "accept_language",
        "session_data",
        "timestamp",
        "request_path",
    )

    def get_search_fields(self, request):
        User = get_user_model()
        return "ip", f"user__{getattr(User, 'USERNAME_FIELD', 'username')}"

    def is_valid(self, obj):
        return obj.expire_date > now()

    is_valid.boolean = True

    def location(self, obj):
        return location(obj.ip)

    def device(self, obj):
        return device(obj.user_agent) if obj.user_agent else ""


admin.site.register(Session, SessionAdmin)
