from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Item,
    Stock,
    Category,
    Order,
    OrderItem,
    ReturnRequestItem,
    ReturnRequest,
)
from .services import generate_pdf, generate_ean_pdf
from ..account.admin import second_admin, core_admin, first_admin


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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        admin_site_filters = {"core_admin": "Zarg", "second_admin": "EV"}
        stock_name = admin_site_filters.get(self.admin_site.name, "Senec")
        return qs.filter(stock__name=stock_name)

    actions = [generate_pdf, generate_ean_pdf]
    list_filter = ("ean", "name", "category", "favorite")

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
        if obj.barcode:
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

    # --- Dictionary for assigning admin sites to filters --- #
    admin_filters = {
        "core_admin": "Zarg",
        "second_admin": "EV",
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # --- Filter based on the admin site name --- #
        filter_name = self.admin_filters.get(self.admin_site.name, "Senec")
        return qs.filter(name=filter_name)


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


class ReturnRequestItemInline(admin.TabularInline):
    model = ReturnRequestItem
    raw_id_fields = ["item"]


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ("employee", "created_at", "updated_at", "reason", "status")
    inlines = [ReturnRequestItemInline]


first_admin.register(Stock, StockAdmin)
first_admin.register(Item, ItemAdmin)
first_admin.register(Category, CategoryAdmin)

second_admin.register(Stock, StockAdmin)
second_admin.register(Item, ItemAdmin)
second_admin.register(Category, CategoryAdmin)

core_admin.register(Stock, StockAdmin)
core_admin.register(Item, ItemAdmin)
core_admin.register(Category, CategoryAdmin)
core_admin.register(Order, OrderAdmin)
core_admin.register(ReturnRequest, ReturnRequestAdmin)
