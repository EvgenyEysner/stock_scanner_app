from django.urls import path

from apps.api.views import (
    ItemsListView,
    ItemDetailView,
    CartAPI,
    OrderApiView,
    OrderItemApiView,
    UserView,
    LoginViewSet,
    RefreshViewSet,
)

urlpatterns = [
    path("user/", UserView.as_view(), name="user"),
    path("items/", ItemsListView.as_view(), name="items"),
    path("item/<slug:ean>/", ItemDetailView.as_view(), name="item"),
    path("orders/", OrderApiView.as_view(), name="orders"),
    path("order-items/", OrderItemApiView.as_view(), name="order-items"),
    path("cart/", CartAPI.as_view(), name="cart"),
    # --------- account urls ------------------ #
    path("login/", LoginViewSet.as_view({"post": "create"})),
    path("refresh/", RefreshViewSet.as_view({"post": "create"})),
]
