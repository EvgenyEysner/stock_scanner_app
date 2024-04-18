from django.urls import path

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
    # --------- account urls ------------------ #
    # path("login/", LoginViewSet.as_view({"post": "create"})),
    # path("refresh/", RefreshViewSet.as_view({"post": "create"})),
]
