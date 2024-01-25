from django.urls import path

from .views import ItemsListView, ItemDetailView

urlpatterns = [
    path("", ItemsListView.as_view(), name="items"),
    path("item/<slug:ean>/", ItemDetailView.as_view(), name="item"),
]
