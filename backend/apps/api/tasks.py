import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage

from apps.api.utils.csv_service import generate_csv, generate_order_list
from apps.warehouse.models import Order


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


@shared_task
def check_stock():
    file = generate_order_list()
    subject = f"Bestand vom |{datetime.datetime.now()}"
    message = "Anbei ist eine Bestandsübersicht"
    from_email = settings.EMAIL_HOST_USER
    recipients = [settings.RECIPIENT_ADDRESS]

    email = EmailMessage(
        subject,
        message,
        from_email,
        recipients,
    )
    email.attach(f"bestandsliste.csv", file.getvalue(), "text/csv")
    email.send(fail_silently=False)
