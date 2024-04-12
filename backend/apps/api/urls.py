from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.api.views import (
    ItemsListView,
    ItemDetailView,
    CartAPI,
    LoginView,
    OrderApiView,
    OrderItemApiView,
)

urlpatterns = [
    path("items/", ItemsListView.as_view(), name="items"),
    path("item/<slug:ean>/", ItemDetailView.as_view(), name="item"),
    path("orders/", OrderApiView.as_view(), name="orders"),
    path("order-items/", OrderItemApiView.as_view(), name="order-items"),
    path("cart/", CartAPI.as_view(), name="cart"),
    # --------- account urls ------------------ #
    path("login/", LoginView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
