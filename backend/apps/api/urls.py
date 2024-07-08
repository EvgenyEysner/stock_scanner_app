from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from apps.api.views import (
    ItemsListView,
    ItemDetailView,
    CartAPI,
    OrderListView,
    OrderItemListView,
    UserView,
)

urlpatterns = [
    path("user/", UserView.as_view(), name="user"),
    path("items/", ItemsListView.as_view(), name="items"),
    path("item/<slug:ean>/", ItemDetailView.as_view(), name="item"),
    path("order/", OrderListView.as_view(), name="order"),
    path("order-items/", OrderItemListView.as_view(), name="order-items"),
    path("cart/", CartAPI.as_view(), name="cart"),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]
