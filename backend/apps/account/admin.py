from django.contrib import admin

from apps.account.models import Employee


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
