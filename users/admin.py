from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import NewUserForm, ChangeUserInfoForm
from .models import User

# admin.site.register(User, UserAdmin)


class CustomUserAdmin(UserAdmin):
    add_form = NewUserForm
    form = ChangeUserInfoForm
    model = get_user_model()
    list_display = ["username", "email", "first_name", "last_name", "is_staff"]
    fieldsets = (
        (("User"), {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


CustomUserAdmin.add_fieldsets = ((None, {"classes": ("wide",), "fields": ("username", "first_name", "last_name", "password1", "password2")}),)

admin.site.register(User, CustomUserAdmin)
