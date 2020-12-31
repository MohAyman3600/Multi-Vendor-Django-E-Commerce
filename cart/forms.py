"""Cart forms."""
from string import Template
from django import forms
from django.utils.safestring import mark_safe

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class QuantityWidget(forms.widgets.Widget):
    """Plus-minus quntity input widget."""

    def render(self, name, value, attrs, renderer):
        html = Template(
            '<input type ="text" value="$value" name="quantity" class="cart-plus-minus-box" >')
        input_html = mark_safe(html.substitute(
            value=1 if value is None else value))
        return input_html


class CartAddProductForm(forms.Form):
    """Form to add products to cart."""
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label="",
        widget=QuantityWidget,
    )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
