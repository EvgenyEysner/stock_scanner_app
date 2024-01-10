from rest_framework import serializers

from ..warehouse.models import Item


class ItemSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(source="get_unit_display")

    class Meta:
        model = Item
        fields = "__all__"
