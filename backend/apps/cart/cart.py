from django.conf import settings

from apps.api.serializers import ItemSerializer
from apps.warehouse.models import Item


class Cart:
    def __init__(self, request):
        """
        initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, item, quantity=1, overide_quantity=False):
        """
        Add item to the cart or update its quantity
        """

        item_id = str(item["id"])
        if item_id not in self.cart:
            self.cart[item_id] = {"quantity": 0}
        if overide_quantity:
            self.cart[item_id]["quantity"] = quantity
        else:
            self.cart[item_id]["quantity"] += quantity
        self.save()

    def remove(self, item):
        """
        Remove a item from the cart
        """
        item_id = str(item["id"])

        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __iter__(self):
        """
        Loop through cart items and fetch the items from the database
        """
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        cart = self.cart.copy()
        for item in items:
            cart[str(item.id)]["item"] = ItemSerializer(item).data
        for item in cart.values():
            item["total"] = item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return (item["quantity"] for item in self.cart.values())

    def get_total(self):
        return (item["quantity"] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
