"""Testing how app components ingerate together."""
import datetime
from users.views import SignUpView, CustomLoginView
from users.views import VendorDetail, CustomerDetail
from users.customer_forms import CustomerCreationForm
from users.vendor_forms import VendorCreationForm

from .helpers import TestData
from django.urls.base import resolve
from django.urls import reverse
from django.test import TestCase
from users.models import CustomerProfile, User, VendorProfile


class SignUpTests(TestCase):

    data = TestData

    def setUp(self):
        self.vendor_url = "{}?user_type=vendor".format(reverse('users:signup'))
        self.customer_url = "{}?user_type=customer".format(
            reverse('users:signup'))

    def test_signup_template(self):
        vendor_resp = self.client.get(self.vendor_url)
        customer_resp = self.client.get(self.customer_url)
        self.assertEqual(vendor_resp.status_code, 200)
        self.assertEqual(customer_resp.status_code, 200)
        self.assertTemplateUsed(vendor_resp, 'account/signup.html')
        self.assertTemplateUsed(customer_resp, 'account/signup.html')
        self.assertContains(vendor_resp, 'Sign Up as a Vendor')
        self.assertContains(customer_resp, 'Sign Up as a Customer')
        self.assertNotContains(
            vendor_resp, 'Hi there! I should not be on the page.')
        self.assertNotContains(
            customer_resp, 'Hi there! I should not be on the page.')

    def test_signup_vendor_form(self):
        vendor_resp = self.client.get(self.vendor_url)
        forms = vendor_resp.context.get('forms')
        self.assertTrue('vendor' in forms)
        self.assertTrue('customer' not in forms)
        self.assertIsInstance(forms.get('vendor'), VendorCreationForm)
        self.assertContains(vendor_resp, 'csrfmiddlewaretoken')

    def test_signup_customer_form(self):
        customer_resp = self.client.get(self.customer_url)
        forms = customer_resp.context.get('forms')
        self.assertTrue('customer' in forms)
        self.assertTrue('vendor' not in forms)
        self.assertIsInstance(forms.get('customer'), CustomerCreationForm)
        self.assertContains(customer_resp, 'csrfmiddlewaretoken')

    def test_signup_view(self):
        view = resolve('/users/signup/')
        self.assertEqual(
            view.func.__name__,
            SignUpView.as_view().__name__
        )


class LogInTests(TestCase):
    """Testing the login view."""

    def setUp(self):
        """Setup login url."""
        self.url = reverse('users:login')

    def test_login_template(self):
        """Test corret template used."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/login.html')
        self.assertContains(resp, 'Log In')
        self.assertNotContains(
            resp, 'Hi there! I should not be on the page.')

    def test_login_permissions(self):
        """Test that permissions and their redirect work."""
        user = User.objects.create_user(
            email='testUser@test.com', password='test123')
        self.client.force_login(user)
        resp = self.client.get(self.url)
        redirect_url = reverse(
            CustomLoginView.permission_denied_redirect,
            kwargs={
                'error_name': CustomLoginView.error_name,
                'error_msg': CustomLoginView.error_msg.safe_substitute(
                    url=reverse("users:logout")
                )
            }
        )
        self.assertRedirects(resp, expected_url=redirect_url)


class VendorDetailTests(TestCase):
    """Testing the VendorDetail view."""

    def setUp(self):
        """Setup login url."""
        self.user = User.objects.create_user(
            email='testUser@email.com',
            password='testpassword123',
        )
        vendor = VendorProfile.objects.create(
            user=self.user,
            first_name='Mohamed',
            last_name='Ayman',
            mobile_number='0111111111',
            address='11th St.',
            country='Egypt',
            date_of_birth=datetime.date(2000, 1, 1),
            company_name='KTS',
            company_website='https://kts.com',
            product_desc='toys',
        )
        self.url = reverse('users:vendorprofile_detail',
                           kwargs={'pk': vendor.id})

    def test_vendor_detail_template(self):
        """Test correct template used."""
        self.client.force_login(self.user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'vendor_detail.html')
        self.assertContains(resp, 'Vendor Dashboard')
        self.assertNotContains(
            resp, 'Hi there! I should not be on the page.')

    def test_vendor_detail_permissions(self):
        """Test that permissions and their redirect work."""
        resp = self.client.get(self.url)
        redirect_url = reverse(
            VendorDetail.permission_denied_redirect,
            kwargs={
                'error_name': VendorDetail.error_name,
                'error_msg': VendorDetail.error_msg
            }
        )
        self.assertRedirects(resp, expected_url=redirect_url)


class CustomerDetailTests(TestCase):
    """Testing the CustomerDetail view."""

    def setUp(self):
        """Setup login url."""
        self.user = User.objects.create_user(
            email='testUser@email.com',
            password='testpassword123',
        )
        customer = CustomerProfile.objects.create(
            user=self.user,
            first_name='Mohamed',
            last_name='Ayman',
            mobile_number='0111111111',
            address='11th St.',
            country='Egypt',
            date_of_birth=datetime.date(2000, 1, 1),
        )
        self.url = reverse('users:customerprofile_detail',
                           kwargs={'pk': customer.id})

    def test_vendor_detail_template(self):
        """Test correct template used."""
        self.client.force_login(self.user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'customer_detail.html')
        self.assertContains(resp, 'Customer Dashboard')
        self.assertNotContains(
            resp, 'Hi there! I should not be on the page.')

    def test_vendor_detail_permissions(self):
        """Test that permissions and their redirect work."""
        resp = self.client.get(self.url)
        redirect_url = reverse(
            CustomerDetail.permission_denied_redirect,
            kwargs={
                'error_name': CustomerDetail.error_name,
                'error_msg': CustomerDetail.error_msg
            }
        )
        self.assertRedirects(resp, expected_url=redirect_url)
