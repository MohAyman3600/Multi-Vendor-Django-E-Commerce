"""Order and Checkout views."""
from decimal import Context
import json
import pdb
from django.http import request
import stripe
from django.http.response import JsonResponse
from orders.models import Order, OrderProduct
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect, render
from django.views.generic import DetailView
from utils.multiformsviews import MultiFormsView
from users.permissions import VendorNotAllowedPermissionMixin
from django.contrib.auth import login as auth_login

from shop.settings import STRIPE_SECRET_KEY, PLATFORM_FEE_PERCENTAGE
from .forms import BillingDetailsForm
from cart.cart import Cart
from users.models import User


class CheckoutView(VendorNotAllowedPermissionMixin, MultiFormsView):

    permission_denied_redirect = 'error'
    form_classes = {
        'login': AuthenticationForm,
        'checkout': BillingDetailsForm,
    }
    prefixes = {
        'login': 'login',
        'checkout': 'checkout',
    }
    success_urls = {
        'login': 'orders:checkout',
        'checkout': 'orders:order_confirmed',
    }
    template_name = "orders/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if isinstance(request.user, User):
            del context['forms']['login']
            customer = request.user.customerprofile
            context['forms']['checkout'].__init__(
                initial={"country": customer.country,
                         "first_name": customer.first_name,
                         "last_name": customer.last_name,
                         "address": customer.address,
                         "email": request.user.email,
                         "phone": customer.mobile_number,
                         })
            return self.render_to_response(context)
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_prefixes = self.get_prefix_from_request(request)
        if 'login' in form_prefixes:
            return self._proccess_individual_form('login')
        return self._proccess_individual_form('checkout')

    def login_form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return redirect(self.get_success_url('login'))

    def checkout_form_valid(self, form):
        cart = Cart(self.request)
        billing_details = form.save(commit=False)
        order = Order.objects.create(
            status=0,
            total_price=cart.get_total_price(),
            paltform_fees_percentage=PLATFORM_FEE_PERCENTAGE,
        )
        for item in cart:
            OrderProduct.objects.create(
                product_id=item['product'].id,
                purchase_price=item['price'],
                product_qty=item['quantity'],
                total_price=item['total_price'],
                order=order,
            )

        billing_details.order = order
        if not isinstance(self.request.user, AnonymousUser):
            order.customer = self.request.user.customerprofile
        try:
            order.customer = User.objects.filter(
                email=self.request.POST['checkout-email']).first()
        except User.DoesNotExist:
            pass
        billing_details.save()
        cart.clear()
        token = self.request.POST.get('stripeToken')
        for product in order.order_product.all():
            process_product_payment(product, STRIPE_SECRET_KEY, token)
        return redirect(self.get_success_url('checkout'), pk=order.id)


def process_product_payment(product, stripe_secret_key, token):
    stripe.api_key = stripe_secret_key
    fee_amount = product.total_price * product.order.paltform_fees_percentage
    try:
        charge = stripe.Charge.create(
            amount=int(product.total_price*100),
            currency='usd',
            source=token,
            application_fee=int(fee_amount*100),
            stripe_account=product.product.vendor.stripe_id,
        )
        if charge:
            product.payment_status = 1
            product.order.charge_code = charge.id
            product.save()
    except stripe.error.StripeError as e:
        product.payment_status = 0
        product.payment_error = e
        product.save()


class OrderConfirmedView(DetailView):
    model = Order
    template_name = "orders/order_confirmed.html"
    context_object_name = 'order'


class OrderDetailView(DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = 'order'


def OrderTrackingView(request):
    if request.method == 'POST':
        tracking_code = request.POST['tracking_code']
        try:
            order = Order.objects.get(tracking_code=tracking_code)
        except Order.DoesNotExist:
            return render(request, 'orders/order_track.html', context={'Founded': 'True'})
        return redirect('orders:order_detail', pk=order.id)
    else:
        return render(request, 'orders/order_track.html', {'Founded': 'False'})
