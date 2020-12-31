"""Order and Checkout forms."""
from django import forms

from .models import BillingDetails


class BillingDetailsForm(forms.ModelForm):
    """Checkout form."""

    class Meta:
        model = BillingDetails
        fields = ("country", "first_name", "last_name", "address", "city",
                  "postcode", "email", "phone", "order_notes",)

        widgets = {
            'address': forms.Textarea(attrs={
                'placeholder': 'Street address.\n\nApartment, suite, unit etc.',
                'rows': '3',
            }),
            'order_notes': forms.Textarea(attrs={
                'placeholder': 'Notes about your order, e.g. special notes for delivery'
            }),
        }
