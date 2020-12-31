"""Custom User Views."""
import stripe
from django.http.response import HttpResponseRedirect
from users.models import CustomerProfile, VendorProfile
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import DetailView
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from shop.settings import (
    USERTYPE_VENDOR,
    USERTYPE_CUSTOMER,
    CART_SESSION_ID,
    STRIPE_SECRET_KEY
)
from .view_helpers import update_vendor_stripe_status
from .customer_forms import CustomerCreationForm
from .vendor_forms import VendorCreationForm
from utils.multiformsviews import MultiFormsView
from .permissions import AnonymousUserRquiredPermissionMixin
from .permissions import UserTypeRquiredPermissionMixin
from cart.cart import Cart


class SignUpView(MultiFormsView):
    """Sign up view for user and associated profile."""

    form_classes = {
        'customer': CustomerCreationForm,
        'vendor': VendorCreationForm,
    }
    prefixes = {
        'vendor': 'vendor',
        'customer': 'customer',
    }
    success_urls = {
        'vendor': 'users:vendorprofile_detail',
        'customer': 'home',
    }
    template_name = 'account/signup.html'

    def get(self, request, *args, **kwargs):
        """
        Return form based on user type.
        Overridden from ProccessMultiFormsView.
        """
        user_type = request.GET.get('user_type')
        if user_type == USERTYPE_VENDOR:
            return self.render_to_response(
                context=self.get_context_data(form_name='vendor'))
        elif user_type == USERTYPE_CUSTOMER:
            return self.render_to_response(
                context=self.get_context_data(form_name='customer'))
        return redirect('home')

    def post(self, request, *args, **kwargs):
        """
        Return form result based on user type.
        Overridden from ProccessMultiFormsView.
        """
        user_type = request.POST.get('user_type', USERTYPE_CUSTOMER)
        if user_type == USERTYPE_VENDOR:
            return self._proccess_individual_form(form_name='vendor')
        else:
            return self._proccess_individual_form(form_name='customer')

    def vendor_form_valid(self, form):
        """
        Save user associated with it's vendor profile.
        Overridden from MultiFormsMixin.
        """
        vendor = form.save()
        auth_login(self.request, vendor.user)
        return redirect(self.get_success_url(form_name='vendor'), pk=vendor.id)

    def customer_form_valid(self, form):
        """
        Save user associated with it's customer profile.
        Overridden from MultiFormsMixin.
        """
        customer = form.save()
        auth_login(self.request, customer.user)
        next = self.request.POST.get('next')
        if next is None or 'signup' in next:
            return redirect(self.get_success_url(form_name='customer'))
        return redirect(next)


class CustomLoginView(AnonymousUserRquiredPermissionMixin, LoginView):
    """Create custom login view to customize the redirect url."""

    permission_denied_redirect = 'error'
    template_name = 'account/login.html'


class CustomLogoutView(AnonymousUserRquiredPermissionMixin, LogoutView):
    """Create custom logout view to customize the redirect url."""

    permission_denied_redirect = 'error'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        cart = Cart(request)
        auth_logout(request)
        self.request.session[CART_SESSION_ID] = cart.__dict__['cart']
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)


class VendorDetail(UserTypeRquiredPermissionMixin, DetailView):
    """View to display vendor information."""

    permission_denied_redirect = 'error'
    user_type_required = USERTYPE_VENDOR
    model = VendorProfile
    template_name = 'users/vendor_detail.html'
    context_object_name = 'vendor'

    def get(self, request, *args, **kwargs):
        """
        Update vendor stripe status before geting the vendor dashboard.
        Used only in local testing environment, in live environment
        the StripeAccountStatusWebHook should handle this; though, not
        tested yet.
        """
        response = super().get(request, *args, **kwargs)
        stripe.api_key = STRIPE_SECRET_KEY
        update_vendor_stripe_status(vendor=self.object)
        return response


class CustomerDetail(UserTypeRquiredPermissionMixin, DetailView):
    """View to display vendor information."""

    permission_denied_redirect = 'error'
    user_type_required = USERTYPE_CUSTOMER
    model = CustomerProfile
    template_name = 'users/customer_detail.html'
    context_object_name = 'customer'
