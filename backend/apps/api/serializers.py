from rest_framework import serializers

from apps.account.models import User
from apps.warehouse.models import Item, Order, OrderItem


class ItemSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(source="get_unit_display")
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


# -------------- accounts serializers --------------- #


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "is_active", "is_staff", "date_joined", "password"]
        read_only_field = ["is_active", "is_staff", "date_joined"]
