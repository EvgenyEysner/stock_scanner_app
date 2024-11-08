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
    unit = serializers.CharField()
    favorite = serializers.CharField()
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    stock = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Item
        fields = "__all__"

    def to_internal_value(self, data):
        # Erstelle eine veränderbare Kopie von `data`
        mutable_data = data.copy()

        # --- Convert the text entries for `unit` and `favorite` into the corresponding integer values --- #
        if "unit" in mutable_data:
            unit_display_map = {v: k for k, v in Item.UnitChoices.choices}
            mutable_data["unit"] = unit_display_map.get(
                mutable_data["unit"], mutable_data["unit"]
            )

        if "favorite" in mutable_data:
            favorite_display_map = {v: k for k, v in Item.ColorSelection.choices}
            mutable_data["favorite"] = favorite_display_map.get(
                mutable_data["favorite"], mutable_data["favorite"]
            )

        return super().to_internal_value(mutable_data)

    def to_representation(self, instance):
        # --- Convert the numerical values back to text --- #
        representation = super().to_representation(instance)
        representation["unit"] = instance.get_unit_display()
        representation["favorite"] = instance.get_favorite_display()
        return representation


# --- This serializes all objects of Order Item model with all fields --- #
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
