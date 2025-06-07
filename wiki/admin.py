
"""Admin customization for the wiki app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Dark Ages", {"fields": ("dark_ages_username", "discord_handle")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Dark Ages", {"fields": ("dark_ages_username", "discord_handle")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
