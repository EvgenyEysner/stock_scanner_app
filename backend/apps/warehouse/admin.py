from django.contrib import admin
from django.utils.html import format_html

from .models import Item, Stock, Category, Order, OrderItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "image_tag",
        "name",
        "description",
        "category",
        "on_stock",
        "min_stock",
        "stock",
        "unit",
        "manufacturer_number",
        "ean",
        "barcode_tag",
        "favorite_color",
    )

    list_filter = ("id", "name", "category")

    @admin.display(description="Favoriten", ordering="favorite")
    def favorite_color(self, obj):
        # ---- Colors based on the favorite value ---- #
        color_map = {1: "#ed102a", 2: "#ede910", 3: "#31ed10"}  # Red  # Yellow  # Green

        # --- Direct return of the HTML only if the favorite value is present in the map --- #
        if color := color_map.get(obj.favorite):
            return format_html(
                '<span class="far fa-circle fa-2x" style="background: {0}; color: {0}"></span>',
                color,
            )
        return

    @admin.display(description="Bild")
    def image_tag(self, obj):
        if obj.image:
            return format_html(
                f'<img src="{obj.image.url}" style="width: 50px; height: 50px;"/>'
            )

    @admin.display(description="Barcode")
    def barcode_tag(self, obj):
        return format_html(
            f'<img src="{obj.barcode.url}" style="width: 50px; height: 50px;"/>'
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
