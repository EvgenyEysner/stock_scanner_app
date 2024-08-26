from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import format_html
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

        OrderItem.objects.bulk_create(order_items_list)
        serializer = OrderSerializer(order, many=False)

        # user = i.order.employee
        # note = i.order.note
        # stock = i.item.stock
        # item_name = i.item.name
        # quantity = i.quantity
        # unit = i.item.unit
        # manufacturer_number = i.item.manufacturer_number

        message = f"""
            Bestellung Lager{[i.item.stock for i in order.items.all()]}
            Bestellnotiz:{[i.order.note for i in order.items.all()]}
            Bezeichnung: {[i.item.name for i in order.items.all()]}
            Menge: {[i.quantity for i in order.items.all()]}
            Messeinheit: {[i.item.unit for i in order.items.all()]}
            Hersteller Artikelnummer: {[i.item.manufacturer_number for i in order.items.all()]}
            """
        subject = f"Bestellung Lager {[i.item.stock for i in order.items.all()]}"
        # message = f"Auftrag erfasst durch: {i.order.employee}, + \n" \
        #           f"Auftragsdaten: {'Artikel': i.item.name}"
        send_mail(
            subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS],
        )

        if not serializer.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------- account views ------------ #
