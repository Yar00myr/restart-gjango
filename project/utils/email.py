from django.urls import reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from shop.models import Order


def send_order_confirmation_email(order: Order):
    subject = f"confirmation order {order.id}"
    context = {"order": order}
    text_context = render_to_string("email/confirmation_email.html", context)
    to_email = order.contact_email
    try:
        send_mail(
            subject,
            text_context,
            settings.DEFAULT_FROM_EMAIL,
            [to_email, settings.ADMIN_EMAIL],
        )
    except Exception as e:
        print(f"Error sending email: {e}")
