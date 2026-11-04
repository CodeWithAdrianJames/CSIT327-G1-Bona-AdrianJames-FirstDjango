from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["first_name", "last_name", "username", "email", "role", "is_staff"]

    fieldsets = UserAdmin.fieldsets + (
        ("School Profile", {"fields": ("role", "course")}),
    )