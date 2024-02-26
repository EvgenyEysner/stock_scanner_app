from decimal import Decimal

from django.conf import settings
from apps.warehouse.models import Item


class Cart:
    def __init__(self, request):
        """
        Initialize the shopping cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in a session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item, quantity=1, override_quantity=False):
        """
        Add an item to your cart or update its quantity.
        """
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {quantity: 0}

        if override_quantity:
            self.cart[item_id]["quantity"] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified",
        # to make sure it stays that way
        self.session.modified = True

    def remove(self, item):
        """
        remove item
        """
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
        self.save()

    def __iter__(self):
        """
        Scroll through the cart items in a loop and
        retrieve items from the database.
        """
        items_ids = self.cart.keys()
        # получить объекты product и добавить их в корзину
        items = Item.objects.filter(id__in=items_ids)
        cart = self.cart.copy()
        for item in items:
            cart[str(item.id)]['product'] = item
        # for item in cart.values():
        #     item['price'] = Decimal(item['price'])
        item['quantity'] = item['quantity']
        yield item

    def clear(self):
        # remove the recycle garbage can from the session
        del self.session[settings.CART_SESSION_ID]
        self.save()

