from django.urls import path

from .views import ItemsListView, ItemDetailView

urlpatterns = [
    path("", ItemsListView.as_view(), name="items"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item"),
]
