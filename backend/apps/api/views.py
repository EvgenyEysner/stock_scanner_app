from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from apps.account.models import User
from apps.api.serializers import (
    ItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserSerializer,
    UserLoginSerializer,
)
from apps.api.validation import validate_password, validate_email
from apps.warehouse.models import Item, Order, OrderItem


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ItemsListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = "ean"


# ---------------- order/orderItems views ------------ #


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AllowAny,)


class OrderItemListView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (AllowAny,)


class CartAPI(APIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    # def get(self, request, format=None):
    #     cart = Cart(request)
    #
    #     return Response(
    #         {"data": list(cart.__iter__()), "cart_total": cart.get_total()},
    #         status=status.HTTP_200_OK,
    #     )

    def post(self, request, *args, **kwargs):
        order_items = request.data
        # Todo SET/GET User
        order = Order.objects.create(employee_id=1, note=order_items["note"])
        order_items_list = []
        for item in order_items["data"]:
            order_items_list.append(
                OrderItem(
                    item_id=item.get("id"), order=order, quantity=item.get("quantity")
                )
            )
            product = Item.objects.get(id=item.get("id"))
            product.on_stock -= item.get("quantity")
            product.save()

        OrderItem.objects.bulk_create(order_items_list)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(status=status.HTTP_400_BAD_REQUEST)

        # print(order_item)
        # order_qs = Order.objects.filter(employee_id=1)
        # if order_qs.exists():
        #     order = order_qs[0]
        #
        #     # check if the order item is in the order
        #     if order.items.filter(item_id=item.id).exists():
        #         order_item.quantity += 1
        #         order_item.save()
        #         return Response(status=status.HTTP_200_OK)
        #     else:
        #         order.items.add(order_item)
        #         return Response(status=status.HTTP_200_OK)
        # else:
        #     ordered_date = timezone.now()
        #     order = Order.objects.create(employee_id=1, modified_at=ordered_date)
        #     order.items.add(order_item)
        #     return Response(status=status.HTTP_200_OK)


# ---------------- account views ------------ #
class UserLogin(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
