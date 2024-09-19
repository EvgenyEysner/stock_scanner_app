import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage

from apps.api.utils.csv_service import (
    generate_csv,
    generate_stock_list,
    generate_return_request,
)
from apps.warehouse.models import Order, ReturnRequest


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
    file = generate_stock_list()
    subject = f"Bestand vom | {datetime.datetime.now().strftime('%d.%m.%Y | %H:%M:%S')}"
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


@shared_task
def return_request_created(return_request_id: int):
    """
    Send e-mail task when return request is created
    """
    return_request = ReturnRequest.objects.get(id=return_request_id)
    file = generate_return_request(return_request.id)

    subject = (
        f"Rückgabe von {return_request.employee} | Retourennummer {return_request.id}"
    )
    message = return_request.reason
    from_email = settings.EMAIL_HOST_USER
    recipients = [settings.RECIPIENT_ADDRESS]

    email = EmailMessage(
        subject,
        message,
        from_email,
        recipients,
    )
    email.attach(f"rückgabe_{return_request.id}.csv", file.getvalue(), "text/csv")
    email.send(fail_silently=False)
