"""Testing Views."""

from users.customer_forms import CustomerCreationForm
from django.test import TestCase

from shop.settings import USERTYPE_VENDOR, USERTYPE_CUSTOMER
from users.vendor_forms import VendorCreationForm
from users.views import CustomLoginView, SignUpView
from users.views import CustomerDetail, VendorDetail
from .helpers import ViewTestingMixin, TestData


class SignUpViewTests(ViewTestingMixin, TestCase):
    """
    Tests for the signup view.

    Tests for the MultiFormsView are implied in this tests,
    yet the view is overriden to display only one form.
    Default behaviour is not tested.
    """

    data = TestData()
    view_class = SignUpView

    def test_get_vendor_signup(self):
        """Test GET-ing the vendor creation form."""
        self.is_callable(data={"user_type": USERTYPE_VENDOR})

    def test_get_customer_signup(self):
        """Test GET-ing the customer creation form."""
        self.is_callable(data={"user_type": USERTYPE_CUSTOMER})

    def test_post_vendor_signup(self):
        """Test POST-ing to the customer creation form."""
        data = self.data.get_vendor_data()
        prefixed_data = {}
        for key, value in data.items():
            prefixed_key = self.view_class.prefixes[USERTYPE_VENDOR]+"-"+key
            prefixed_data[prefixed_key] = value
        prefixed_data["user_type"] = USERTYPE_VENDOR
        self.is_callable(
            post=True,
            data=prefixed_data,
            redirect_to=self.view_class.success_urls[USERTYPE_VENDOR]
        )

    def test_post_customer_signup(self):
        """Test POST-ing to the customer creation form."""
        data = self.data.get_customer_data()
        prefixed_data = {}
        for key, value in data.items():
            prefixed_key = self.view_class.prefixes[USERTYPE_CUSTOMER]+"-"+key
            prefixed_data[prefixed_key] = value
        prefixed_data["user_type"] = USERTYPE_CUSTOMER
        self.is_callable(
            post=True,
            data=prefixed_data,
            redirect_to=self.view_class.success_urls[USERTYPE_CUSTOMER]
        )


class CustomLoginViewTests(ViewTestingMixin, TestCase):
    """
    Testing login view permissions and redirection.

    Only the perrmisions are tested because the view inherts
    the login behaviour from the Django built-in LoginView.
    """
    data = TestData()
    view_class = CustomLoginView

    def setUp(self):
        data = self.data.get_customer_data()
        form = CustomerCreationForm(data=data)
        form.is_valid()
        self.user_customer = form.save()
        self.redirect_to = self.view_class.permission_denied_redirect

    def test_get(self):
        """Test perrmissoin denied if logged in user tries to GET."""
        self.is_callable(user=self.user_customer.user,
                         post=True,
                         redirect_to=self.redirect_to
                         )

    def test_post(self):
        """Test perrmissoin denied if logged in user tries to POST."""
        self.is_callable(user=self.user_customer.user,
                         post=True,
                         redirect_to=self.redirect_to,
                         data={
                             'username': self.user_customer.user.email,
                             'password': self.user_customer.user.password,
                         })


class VendorDetailTests(ViewTestingMixin, TestCase):
    """Testin the vendor detail permissions."""

    data = TestData()
    view_class = VendorDetail

    def setUp(self):
        """
        Set up vendor and customer users for testing,
        and redirection url.
        """
        customer_data = self.data.get_customer_data()
        vendor_data = self.data.get_vendor_data()
        form = CustomerCreationForm(data=customer_data)
        form.is_valid()
        self.user_customer = form.save()
        form = VendorCreationForm(data=vendor_data)
        form.is_valid()
        self.user_vendor = form.save()
        self.redirect_to = self.view_class.permission_denied_redirect

    def test_get(self):
        """Test GET-ing vendor detail."""
        self.is_callable(user=self.user_vendor.user,
                         pk=self.user_vendor.user.id)

    def test_get_denied(self):
        """Test when customer user tries to enter vendor detail."""
        self.is_callable(user=self.user_customer.user,
                         redirect_to=self.redirect_to)


class CustomerDetailTests(ViewTestingMixin, TestCase):
    """Testin the Customer detail permissions."""

    data = TestData()
    view_class = CustomerDetail

    def setUp(self):
        """
        Set up customer and vendor users for testing,
        and redirection url.
        """
        customer_data = self.data.get_customer_data()
        vendor_data = self.data.get_vendor_data()
        form = CustomerCreationForm(data=customer_data)
        form.is_valid()
        self.user_customer = form.save()
        form = VendorCreationForm(data=vendor_data)
        form.is_valid()
        self.user_vendor = form.save()
        self.redirect_to = self.view_class.permission_denied_redirect

    def test_get(self):
        """Test GET-ing the customer detail"""
        self.is_callable(user=self.user_customer.user,
                         pk=self.user_vendor.user.id)

    def test_get_denied(self):
        """Test when vendor user tries to enter customer detail."""
        self.is_callable(user=self.user_vendor.user,
                         redirect_to=self.redirect_to)
