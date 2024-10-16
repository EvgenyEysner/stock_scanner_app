from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.shortcuts import render

from apps.account.forms import CustomUserChangeForm, CustomUserCreateForm
from apps.account.models import Employee, User


# ----- Create a custom AdminSite ----- #
class StartAdminSite(admin.AdminSite):

    def index(self, request, extra_context=None):
        context = {
            "title": "Admin Dashboard",
            "custom_buttons": [
                {
                    "url": "/zarg-admin/",
                    "name": "Zarg Admin",
                    "logo": "image/logo256x256.png",
                },
                {
                    "url": "/energieversum-admin/",
                    "name": "Universum Admin",
                    "logo": "image/energieversum.png",
                },
            ],
        }
        return render(request, "admin/custom_index.html", context)


# ----- Register the admin pages ----- #
class CoreAdmin(admin.AdminSite):
    site_header = "Zarg Lagerverwaltung"
    site_title = "Stocky"
    site_logo = "image/logo256x256.png"


class SecondAdmin(admin.AdminSite):
    site_header = "Lager Energieversum"
    site_title = "Stocky"
    site_logo = "image/energieversum.png"


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ("user__email", "first_name", "last_name")
    list_display = (
        # "employee_link",
        "employee_name",
        "permission_group",
        # "user__is_active",
    )

    list_filter = (
        "user__is_active",
        "permission_group",
    )

    # readonly_fields = (
    #     "team_manager_in_stock",
    # )

    @admin.display(description="Mitarbeiter")
    def employee_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreateForm
    list_display = (
        "email",
        "is_active",
        "date_joined",
        "is_staff",
    )
    ordering = ("email",)
    list_filter = ("is_active",)
    search_fields = ("email",)
    readonly_fields = ("last_login",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "last_login",
                    "is_active",
                    "is_superuser",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_superuser",
                ),
            },
        ),
    )

    @admin.display(
        description="Personal-Nr.",
        ordering="employee__personnel_number",
        empty_value="-",
    )
    def personnel_number(self, obj):
        if hasattr(obj, "employee"):
            return obj.employee.personnel_number

    @admin.display(description="Vorname", ordering="employee__first_name")
    def first_name(self, obj):
        if not hasattr(obj, "employee"):
            return "-"
        return obj.employee.first_name

    @admin.display(description="Nachname", ordering="employee__last_name")
    def last_name(self, obj):
        if not hasattr(obj, "employee"):
            return "-"
        return obj.employee.last_name

    @admin.display(description="Admin", ordering="is_superuser", boolean=True)
    def is_admin(self, obj):
        return obj.is_superuser

    @admin.display(description="Backend-Zugang", boolean=True)
    def is_staff(self, obj):
        return obj.is_staff


# ----- Register models for the new AdminSite ----- #
custom_admin_site = StartAdminSite(name="start_admin")
second_admin = SecondAdmin(name="second_admin")
