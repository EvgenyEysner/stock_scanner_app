import os
from io import BytesIO

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.html import format_html
from xhtml2pdf import pisa

from .models import (
    Item,
    Stock,
    Category,
    Order,
    OrderItem,
    ReturnRequestItem,
    ReturnRequest,
)


def fetch_pdf_resources(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    static_url = settings.STATIC_URL  # Typically /static/
    static_root = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    media_url = settings.MEDIA_URL  # Typically /static/media/
    media_root = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(media_url):
        path = os.path.join(media_root, uri.replace(media_url, ""))
    elif uri.startswith(static_url):
        path = os.path.join(static_root, uri.replace(static_url, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)
    return path


@admin.action(description="PDF Druck")
def generate_pdf(modeladmin, request, queryset):

    template_path = "pdf/report.html"
    context = {
        "items": queryset,
    }
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    # create a pdf
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")),
        result,
        encoding="UTF-8",
        link_callback=fetch_pdf_resources,
    )

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")

    return None


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

    actions = [generate_pdf]
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


class ReturnRequestItemInline(admin.TabularInline):
    model = ReturnRequestItem
    raw_id_fields = ["item"]


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ("employee", "created_at", "updated_at", "reason", "status")
    inlines = [ReturnRequestItemInline]

    # @admin.display(description="Erfasste Menge")
    # def total(self, obj):
    #     return obj.get_total()
