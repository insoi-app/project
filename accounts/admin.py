from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fieldsets for viewing and editing a user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fieldsets for adding a user
    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'password1', 'password2')}),
    )

    # List display fields
    list_display = ['email', 'username', 'is_staff', 'is_active']

admin.site.register(CustomUser, CustomUserAdmin)
