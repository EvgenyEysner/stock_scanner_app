from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import ItemsListView, ItemDetailView, CartAPI, LoginView

urlpatterns = [
    path("", ItemsListView.as_view(), name="items"),
    path("item/<slug:ean>/", ItemDetailView.as_view(), name="item"),
    path("cart", CartAPI.as_view(), name="cart"),
    # --------- account urls ------------------ #
    path("login/", LoginView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
