from rest_framework import serializers

from apps.warehouse.models import Item


class ItemSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(source="get_unit_display")
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    stock = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Item
        fields = "__all__"
