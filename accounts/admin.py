from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserInfo

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("name",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("name",)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserInfo)