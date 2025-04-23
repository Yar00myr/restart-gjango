from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["contact_name", "contact_email", "contact_phone", "address"]
        labels = {
            "contact_name": "Your name",
            "contact_email": "Your email",
            "contact_phone": "Your phone",
            "address": "Your address",
        }
