from django.views.generic import ListView

from apps.warehouse.models import Item


class EanView(ListView):
    model = Item
    context_object_name = "items"
    template_name = "pdf/ean.html"
