"""Orders app url configratoin."""
from django.urls import path

from .views import CheckoutView, OrderConfirmedView, OrderDetailView, OrderTrackingView

app_name = 'orders'

urlpatterns = [
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('order_confirmed/<int:pk>/', OrderConfirmedView.as_view(),
         name='order_confirmed'),
    path('order_detail/<int:pk>/', OrderDetailView.as_view(),
         name='order_detail'),
    path('order_tracking/',
         OrderTrackingView, name='order_track'),
]
