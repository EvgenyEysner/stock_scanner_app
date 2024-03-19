from typing import List

from django.contrib.auth.models import ContentType, Permission
from rest_framework.permissions import BasePermission, DjangoModelPermissions


def perms(model, actions: List[str]):
    """Helper function, which makes the notation of model permissions a bit more compact (see below)."""
    content_type = ContentType.objects.get_for_model(model, for_concrete_model=False)
    all_permissions = []

    for action in actions:
        # Add default permissions "View", "Change", "Add", "Delete"
        permissions = Permission.objects.filter(
            content_type=content_type, codename__contains=action
        )

        # If action was not a default permission add custom permission.
        if not permissions:
            permissions = [
                Permission.objects.create(
                    content_type=content_type, codename=action, name=action
                )
            ]

        all_permissions += permissions

    return all_permissions


def is_staff(employee):
    """Determine if employee has backend access."""
    return employee.permission_group != employee.PermissionGroup.CARETAKER


def is_limited_by_stock(employee):
    """Determine if"""
    return employee.permission_group in (
        employee.PermissionGroup.BACKOFFICE,
        employee.PermissionGroup.STOCK_MANAGEMENT,
        employee.PermissionGroup.TEAM_MANAGEMENT,
    )


def set_group_permissions(sender, instance, **kwargs):
    """Signal handler, for the post_save signal"""
    from apps.account.models import (
        Employee,
        User,
    )
    from apps.warehouse.models import Stock, Item, Category, Order

    group_permissions = {
        Employee.PermissionGroup.BACKOFFICE: [
            perms(Item, ["view", "change", "add", "delete"]),
            perms(Employee, ["view", "change", "add", "delete"]),
            perms(Stock, ["view", "change", "add", "delete"]),
            perms(User, ["view", "change", "add", "delete"]),
            perms(Order, ["view", "change", "add", "delete"]),
            perms(Category, ["view", "change", "add", "delete"]),
        ],
        Employee.PermissionGroup.STOCK_MANAGEMENT: [
            perms(Item, ["view", "change", "add", "delete"]),
            perms(Employee, ["view"]),
            perms(Stock, ["view", "change", "add"]),
            perms(User, []),
            perms(Order, ["view", "change", "add", "delete"]),
            perms(Category, ["view", "change", "add", "delete"]),
        ],
        Employee.PermissionGroup.TEAM_MANAGEMENT: [
            perms(Item, ["view", "change", "add"]),
            perms(Employee, ["view"]),
            perms(Stock, ["view"]),
            perms(User, []),
            perms(Order, ["view", "change", "add"]),
            perms(Category, ["view"]),
        ],
        Employee.PermissionGroup.INSTALLER: [
            perms(Item, ["view", "add"]),
            perms(Employee, []),
            perms(Stock, ["view"]),
            perms(User, []),
            perms(Order, ["view"]),
            perms(Category, ["view"]),
        ],
    }

    instance.user.user_permissions.clear()

    if permissions := group_permissions.get(instance.permission_group):
        for model_permissions in permissions:
            instance.user.user_permissions.add(*model_permissions)


class IsSpecifiedUserPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            has_api_permission = request.user.id == int(view.kwargs["user_id"])
        except ValueError:
            return False

        return has_api_permission


class ModelPermissionsAndIsSpecifiedUser(DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    def has_permission(self, request, view):
        has_model_permission = super().has_permission(request, view)

        try:
            has_api_permission = request.user.id == int(view.kwargs["user_id"])
        except ValueError:
            return False

        return has_model_permission and has_api_permission
