from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    ItemSerializer,
    MyTokenObtainPairSerializer,
    OrderSerializer,
    OrderItemSerializer,
)
from ..cart.cart import Cart
from ..warehouse.models import Item, Order, OrderItem


class ItemsListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetailView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = "ean"


# ---------------- order/orderItems views ------------ #


class OrderApiView(APIView):
    queryset = Order.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemApiView(APIView):
    queryset = OrderItem.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        orders = OrderItem.objects.all()
        serializer = OrderItemSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartAPI(APIView):
    """
    Single API to handle cart operations
    """

    permission_classes = (AllowAny,)
    queryset = Order.objects.all()

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
            print(product)
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


# ---------------- account views ------------ #
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
