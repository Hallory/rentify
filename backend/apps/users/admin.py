from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'username','first_name','last_name')
    ordering = ('email',)
    
    fieldsets = UserAdmin.fieldsets + (
        ("Custom fields", {"fields": ("role", "image")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom fields", {"fields": ("email", "role", "image")}),
    )