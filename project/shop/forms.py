from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices={
            "liqpay": "With LiqPay",
            "monopay": "MonoPay",
            "google": "Google Pay",
            "cash": "With cash",
        }
    )

    class Meta:
        model = Order
        fields = [
            "contact_name",
            "contact_email",
            "contact_phone",
            "address",
            "payment_method",
        ]
        labels = {
            "contact_name": "Your name",
            "contact_email": "Your email",
            "contact_phone": "Your phone",
            "address": "Your address",
            "payment_method": "Payment Method",
        }
