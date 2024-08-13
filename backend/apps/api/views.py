from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.models import User
from apps.api.serializers import (
    ItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserSerializer,
)
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
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order_items = request.data
        order = Order.objects.create(
            employee_id=request.user.employee.id, note=order_items["note"]
        )
        order_items_list = []
        for item in order_items["data"]["cart"]:
            order_items_list.append(
                OrderItem(
                    item_id=item.get("id"), order=order, quantity=item.get("quantity")
                )
            )
            product = Item.objects.get(id=item.get("id"))
            product.on_stock -= item.get("quantity")
            product.save()

            # ---------------- Send mail with order data ------------ #
            subject = f"Bestellung Lager {item.get('stock')}"
            message = f"Auftrag erfasst durch: {order.employee}, + \n" \
                      f"Auftragsdaten: {[item for item in order_items['data']['cart']]}"
            send_mail(
                subject,
                message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.RECIPIENT_ADDRESS],
            )

        OrderItem.objects.bulk_create(order_items_list)
        serializer = OrderSerializer(order, many=False)

        if not serializer.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------- account views ------------ #
