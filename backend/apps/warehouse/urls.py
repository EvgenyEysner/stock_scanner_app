from django.urls import path

from apps.warehouse.views import EanView

urlpatterns = [
    path("eans/", EanView.as_view(), name="ean"),
]
