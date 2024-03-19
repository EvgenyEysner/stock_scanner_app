from django.contrib import admin
from django.utils.html import format_html

from .models import Item, Stock, Category, Order, OrderItem


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
        "on_stock",
        "stock",
        "unit",
        "position_number",
        "manufacturer_number",
        "ean",
        "barcode_tag",
    )

    list_filter = (
        "id",
        "name",
    )


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "manager",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["item"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("employee", "created_at", "modified_at", "note", "total")
    inlines = [OrderItemInline]

    @admin.display(description="Erfasste Menge")
    def total(self, obj):
        return obj.get_total()
