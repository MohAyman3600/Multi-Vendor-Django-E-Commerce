"""Mixins and heloper classes to ease testing."""
from django.http import Http404

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import Resolver404, resolve
from django.contrib.sessions.middleware import SessionMiddleware


class ViewTestingMixin(object):
    """Mixin with shourtcuts for view testing."""

    view_class = None

    def get_view_kwargs(self):
        """
        Return a dictionary representing view kwargs.

        Override this to pass kwargs to the view.
        """
        return {}

    def get_response(self, method, user, data, *args, **kwargs):
        """
        Create a request and passes it to view_class
        returning a response object.
        """
        factory = RequestFactory()
        req_kwargs = {}
        if data:
            req_kwargs.update(data)
        req = getattr(factory, method)('/', data=req_kwargs)
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.user = user if user else AnonymousUser()
        return self.view_class.as_view()(req, *args, pk=1)

    def is_callable(self, user=None, post=False, redirect_to=None, data={},
                    status_code=200, *args, **kwargs):
        """
        Call the view and tests the result.
        And checks redirection status, using 'to' paramter, if exists.
        """
        view_kwargs = kwargs or self.get_view_kwargs()
        if post:
            resp = self.get_response(
                'post', user, data, args=args, kwargs=view_kwargs)
        else:
            resp = self.get_response(
                'get', user, data, args=args, kwargs=view_kwargs)
        if redirect_to:
            self.assertIn(resp.status_code, [
                301, 302], msg="The request was not redirected")
            try:
                resolved_url = resolve(
                    resp.url.split('?')[0].split('#')[0])
                if resolved_url.namespace:
                    url_pattren = (resolved_url.namespace
                                   + ":"+resolved_url.url_name)
                else:
                    url_pattren = resolved_url.url_name
                self.assertEqual(
                    url_pattren,
                    redirect_to, msg='Should redirect to "{}".'.format(
                        redirect_to)
                )
            except Resolver404:
                raise Exception('Could not resolve "{}".'.format(resp.url))
        else:
            self.assertEqual(resp.status_code, status_code)
        return resp

    def is_not_callable(self, **kwargs):
        """Check if the call raises 404."""
        with self.assertRaises(Http404):
            self.is_callable(**kwargs)


class TestData(object):
    """Contains data used for testing."""
    vendor_data = {
        'email': 'testVendor@email.com',
        'first_name': 'Mohamed',
        'last_name': 'Ayman',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'mobile_number': '011111111111',
        'address': '11th St.',
        'country': 'Egypt',
        'company_name': 'KTS',
        'company_website': 'https:kts.com',
        'product_desc': 'toys',
    }

    customer_data = {
        'email': 'testCustomer@email.com',
        'first_name': 'Mohamed',
        'last_name': 'Ayman',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'mobile_number': '011111111111',
        'address': '11th St.',
        'country': 'Egypt',
    }

    def get_vendor_data(self):
        """Vendor Data Getter."""
        return self.vendor_data

    def get_customer_data(self):
        """Customer Data Getter."""
        return self.customer_data
