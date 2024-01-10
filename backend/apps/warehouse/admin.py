from django.contrib import admin
from django.utils.html import format_html

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html(
            f'<img src="{obj.image.url}" style="width: 50px; height: 50px;"/>'
        )

    def barcode_tag(self, obj):
        return format_html(
            f'<img src="{obj.barcode.url}" style="width: 50px; height: 50px;"/>'
        )

    list_display = (
        "image_tag",
        "name",
        "description",
        "stock",
        "unit",
        "position_number",
        "ean",
        "barcode_tag",
    )
