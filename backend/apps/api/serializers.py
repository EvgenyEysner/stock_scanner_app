from rest_framework import serializers

from apps.account.models import User
from apps.warehouse.models import (
    Item,
    Order,
    OrderItem,
    ReturnRequestItem,
    ReturnRequest,
)


class ItemSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(source="get_unit_display")
    favorite = serializers.CharField(source="get_favorite_display")
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    stock = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Item
        fields = "__all__"


# This serializes all objects of Order Item model with all fields
class OrderItemSerializer(serializers.ModelSerializer):
    item = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    employee = serializers.SlugRelatedField(slug_field="last_name", read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


# -------------- return request serializers --------------- #
class ReturnRequestItemSerializer(serializers.ModelSerializer):
    item = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = ReturnRequestItem
        fields = "__all__"


class ReturnRequestSerializer(serializers.ModelSerializer):
    items = ReturnRequestItemSerializer(many=True)
    employee = serializers.SlugRelatedField(slug_field="last_name", read_only=True)

    class Meta:
        model = ReturnRequest
        fields = "__all__"


# -------------- accounts serializers --------------- #
class UserSerializer(serializers.ModelSerializer):
    perms = serializers.SerializerMethodField(read_only=True)

    def get_perms(self, obj):
        return hasattr(obj, "employee") and obj.employee.permission_group

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "is_active",
            "is_staff",
            "date_joined",
            "password",
            "employee",
            "perms",
        ]
        read_only_field = ["is_active", "is_staff", "is_superuser", "date_joined"]
