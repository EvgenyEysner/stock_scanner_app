import csv
import io

from apps.warehouse.models import Order


def generate_csv(order_id: int):
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
