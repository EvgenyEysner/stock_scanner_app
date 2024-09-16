import csv
import io
from typing import List, TextIO

from apps.warehouse.models import Order, Item, ReturnRequest


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


def generate_return_request(return_request_id: int) -> io.StringIO:

    return_request = ReturnRequest.objects.get(id=return_request_id)
    file = io.StringIO()
    writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_ALL)
    writer.writerow(("Bezeichnung", "Menge", "Lager", "EAN", "Rückgabegrund"))

    for return_request_item in return_request.items.all():
        writer.writerow(
            (
                return_request_item.item.name,
                return_request_item.quantity,
                return_request_item.item.stock,
                return_request_item.item.ean,
                return_request_item.return_request.reason,
            )
        )
    file.seek(0)
    return file


def generate_stock_list() -> io.StringIO:
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
        if item.on_stock <= item.min_stock:
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
