from django.urls import reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from shop.models import Order


def send_confirmation_mail(request, user, email, confirm_email: str) -> None:
    confirm_url = request.build_absolute_uri(reverse(f"account:{confirm_email}"))
    confirm_url += f"?user={user.id}&email={email}"
    subject = "Confirm new email"
    message = f"Hello, {user.username} you want to confirm your email? To confirm your email click on: {confirm_url}"
    send_mail(
        subject,
        message,
        "noreply@gmail.com",
        [email],
        fail_silently=False,
    )
    messages.info(request, "Confirmation mail was send.")


def send_order_confirmation_email(order: Order):
    subject = f"confirmation order {order.id}"
    order_total = sum(item.total_price for item in order.items.all())
    context = {"order": order, "order_total": order_total}
    text_context = render_to_string("account/emails/confirmation_email.txt", context)
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
