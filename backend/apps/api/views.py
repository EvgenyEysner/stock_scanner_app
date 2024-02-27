from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ItemSerializer
from ..cart.cart import Cart
from ..warehouse.models import Item


class ItemsListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetailView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = "ean"


class CartAPI(APIView):
    """
    Single API to handle cart operations
    """

    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {"data": list(cart.__iter__()), "cart_total": cart.get_total()},
            status=status.HTTP_200_OK,
        )

    def post(self, request, **kwargs):
        cart = Cart(request)

        if "remove" in request.data:
            product = request.data["item"]
            cart.remove(product)

        elif "clear" in request.data:
            cart.clear()

        else:
            product = request.data
            cart.add(
                item=product["item"],
                quantity=product["quantity"],
                overide_quantity=(
                    product["overide_quantity"]
                    if "overide_quantity" in product
                    else False
                ),
            )

        return Response({"message": "cart updated"}, status=status.HTTP_202_ACCEPTED)
