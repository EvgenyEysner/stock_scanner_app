import csv
import io
from typing import List, TextIO

from apps.warehouse.models import Order, Item


def generate_csv(order_id: int) -> io.StringIO:
    order = Order.objects.get(id=order_id)
    file = io.StringIO()
    writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_ALL)
    writer.writerow(
        (
            "Bezeichnung",
            "Menge",
            "Lager",
            "EAN",
        )
    )
    for order_item in order.items.all():
        writer.writerow(
            (
                order_item.item.name,
                order_item.quantity,
                order_item.item.stock,
                order_item.item.ean,
            )
        )
    file.seek(0)
    return file


def generate_order_list() -> io.StringIO:
    file = io.StringIO()
    writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_ALL)
    writer.writerow(
        (
            "Bezeichnung",
            "Hersteller Artikel",
            "Menge",
            "Lager",
            "EAN",
        )
    )
    for item in Item.objects.all():
        if item.on_stock <= 1:
            writer.writerow(
                (
                    item.name,
                    item.manufacturer_number,
                    item.on_stock,
                    item.stock,
                    item.ean,
                )
            )
    file.seek(0)
    return file
