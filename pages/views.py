"""Main pages views."""
from datetime import datetime, timedelta
from django.views.generic import TemplateView


from products.models import Product
from cart.forms import CartAddProductForm


class HomePageView(TemplateView):
    """Home Template View for displaying home page."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """
        Add featured products and products added since last week to context.
        """
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_featured=True)
        last_week_date = datetime.now() - timedelta(weeks=1)
        context['latest_products'] = Product.objects.filter(
            add_date__gt=last_week_date)
        context['cart_add_form'] = CartAddProductForm()
        return context


class ErrorPageView(TemplateView):
    """Error Page view."""

    template_name = 'error.html'
