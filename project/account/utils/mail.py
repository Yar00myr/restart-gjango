from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail


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
