from django.db import transaction
from django.http import Http404
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.models import User
from apps.api.serializers import (
    ItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserSerializer,
    ReturnRequestSerializer,
    ReturnRequestItemSerializer,
)
from apps.api.tasks import order_created, return_request_created
from apps.warehouse.models import (
    Item,
    Order,
    OrderItem,
    ReturnRequest,
    ReturnRequestItem,
    Category,
    Stock,
)


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 300


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserMeView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return self.request.user
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ItemsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = Pagination


class ItemDetailView(APIView):
    """
    Retrieve and update instance.
    """

    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = "ean"

    def get_object(self, ean):
        try:
            return Item.objects.get(ean=ean)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, ean):
        item = self.get_object(ean)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, ean):
        item = self.get_object(ean)
        data = request.data
        # --- transaction.atomic() block ensures that either all or no changes are made to the database. --- #
        with transaction.atomic():
            # --- Update category if necessary --- #
            if item.category.name != data["category"]:
                category = get_object_or_404(Category, name=data["category"])
                item.category = category

            # --- Update stock if necessary --- #
            if item.stock.name != data["stock"]:
                stock = get_object_or_404(Stock, name=data["stock"])
                item.stock = stock

            favorite_choice = {color: num for num, color in item.ColorSelection.choices}
            unit_choice = {name: num for num, name in item.UnitChoices.choices}

            # --- Update favorite if necessary --- #
            if favorite_choice.get(data["favorite"]) != item.get_favorite_display():
                item.favorite = favorite_choice.get(data["favorite"])

            if unit_choice.get(data["unit"]) != item.get_unit_display():
                item.unit = unit_choice.get(data["unit"])

            # --- Save and validate the updated item --- #
            serializer = ItemSerializer(item, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemCreateView(APIView):

    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        data = request.data

        # --- transaction.atomic() block ensures that either all or no changes are made to the database. --- #
        with transaction.atomic():
            # --- Validate and create the category if it exists --- #
            category = get_object_or_404(Category, name=data.get("category"))
            stock = get_object_or_404(Stock, name=data.get("stock"))

            item = Item(
                image=data.get("image"),
                name=data.get("name"),
                description=data.get("description"),
                category=category,
                stock=stock,
                on_stock=data.get("on_stock"),
                ean=data.get("ean"),
                unit=data.get("unit"),
                favorite=data.get("favorite"),
            )

            # --- Save and validate the new item --- #
            serializer = ItemSerializer(item, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- order/orderItems views ------------ #
class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class OrderItemListView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (IsAuthenticated,)


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

        OrderItem.objects.bulk_create(order_items_list)
        serializer = OrderSerializer(order, many=False)

        # ---------------- Send mail with order data ------------ #
        order_created.delay(order.id)

        if not serializer.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------- ReturnRequest/ReturnRequestItems views ------------ #
class ReturnRequestListView(generics.ListAPIView):
    queryset = ReturnRequest.objects.all()
    serializer_class = ReturnRequestSerializer
    permission_classes = (IsAuthenticated,)


class ReturnRequestItemListView(generics.ListAPIView):
    queryset = ReturnRequestItem.objects.all()
    serializer_class = ReturnRequestItemSerializer
    permission_classes = (IsAuthenticated,)


class ReturnRequestAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return_request_items = request.data
        return_request = ReturnRequest.objects.create(
            employee_id=request.user.employee.id, reason=return_request_items["note"]
        )

        return_request_list = []
        for item in return_request_items["data"]["returns"]:
            return_request_list.append(
                ReturnRequestItem(
                    item_id=item.get("id"),
                    return_request=return_request,
                    quantity=item.get("quantity"),
                )
            )

        ReturnRequestItem.objects.bulk_create(return_request_list)
        serializer = ReturnRequestSerializer(return_request, many=False)

        # ---------------- Send mail with return request data ------------ #
        return_request_created.delay(return_request.id)

        if not serializer.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
