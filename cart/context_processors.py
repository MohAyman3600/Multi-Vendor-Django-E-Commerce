"""Cart context processor."""
from .cart import Cart


def cart(request):
    """Add cart to all template context."""
    return {'cart': Cart(request)}
