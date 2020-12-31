"""Vendor Stripe views."""
import stripe
import json
from django.http.response import HttpResponse
from django.views.generic.base import View
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from shop.settings import STRIPE_SECRET_KEY, USERTYPE_VENDOR
from .models import VendorProfile
from .permissions import UserTypeRquiredPermissionMixin
from .view_helpers import (
    create_stripe_onboarding_link,
    update_vendor_stripe_status
)


class StripeAuthorizeView(UserTypeRquiredPermissionMixin, View):
    """View sending users to Stripe connect onboarding flow."""

    permission_denied_redirect = 'error'
    user_type_required = USERTYPE_VENDOR

    def get(self, request):
        """Redirect to Stripe connect onboarding"""
        user = request.user
        stripe.api_key = STRIPE_SECRET_KEY
        vendor = request.user.vendorprofile
        if vendor.stripe_status == 3:
            account_links = create_stripe_onboarding_link(
                request, vendor.stripe_id)
        else:
            account = stripe.Account.create(
                type='standard',
                email=user.email,
                business_type=None,
            )
            vendor.stripe_id = account.id
            vendor.save()
            account_links = account_links = create_stripe_onboarding_link(
                request, vendor.stripe_id)
        return redirect(account_links.url)


class StripeAuthorizeCallBackView(View):
    """View handling users returning from Stripe connect onboarding."""

    def get(self, request, *args, **kwargs):
        """
        Set stripe status for vendors returning from connect onbording.
        Redirect to vendor dashboard.
        """
        vendor = request.user.vendorprofile
        stripe.api_key = STRIPE_SECRET_KEY
        vendor = request.user.vendorprofile
        update_vendor_stripe_status(vendor)
        vendor_pk = vendor.id
        return redirect("users:vendorprofile_detail",
                        pk=vendor_pk)


@require_POST
@csrf_exempt
def StripeAccountStatusWebHook(request):
    """
    WebHook View triggered when connected account updated.
    Updates the vendor stripe_status when triggered.
    """
    stripe.api_key = STRIPE_SECRET_KEY
    payload = request.body
    event = None
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    # Handle the event
    if event.type == 'account.updated':
        vendor_stripe_profile = event.data.object
        vendor = VendorProfile.objects.get(stripe_id=vendor_stripe_profile.id)
        update_vendor_stripe_status(vendor)
    else:
        print('Unhandled event type {}'.format(event.type))
    return HttpResponse(status=200)
