"""Views helper functions."""

import stripe
from django.shortcuts import reverse


def create_stripe_onboarding_link(request, stripe_id=None,):
    """Creates stripe connect onboarding link by calling Stripe API."""
    account_links = stripe.AccountLink.create(
        account=stripe_id,
        return_url=request.build_absolute_uri(
            reverse("users:stripe_callback")
        ),
        refresh_url=request.build_absolute_uri(
            reverse("users:stripe_authorize")
        ),
        type="account_onboarding",
    )
    return account_links


def update_vendor_stripe_status(vendor):
    """Call stripe API and set vendor stripe_status."""
    vendor_stripe_id = vendor.stripe_id
    vendor_stripe_profile = stripe.Account.retrieve(vendor_stripe_id)
    if vendor_stripe_profile['requirements']['disabled_reason'] == 'requirements.past_due':
        vendor.stripe_status = 3
    elif vendor_stripe_profile['details_submitted'] and vendor_stripe_profile['charges_enabled']:
        vendor.stripe_status = 0
    elif vendor_stripe_profile['details_submitted']:
        vendor.stripe_status = 1
    else:
        vendor.stripe_status = 4
    vendor.save()
