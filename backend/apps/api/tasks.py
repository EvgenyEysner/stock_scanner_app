import csv
import io

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage

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


@shared_task
def order_created(order_id: int):
    """
    Send e-mail task when order is created
    """
    order = Order.objects.get(id=order_id)
    file = generate_csv(order.id)

    subject = f"Auftrag von {order.employee}| Auftragsnummer {order.id}"
    message = order.note
    from_email = settings.EMAIL_HOST_USER
    recipients = [settings.RECIPIENT_ADDRESS]

    email = EmailMessage(
        subject,
        message,
        from_email,
        recipients,
    )
    email.attach(f"auftrag_{order.id}.csv", file.getvalue(), "text/csv")
    email.send(fail_silently=False)
