"""Testing Admin."""
import datetime
from django.contrib import admin
from django.contrib.sessions.middleware import SessionMiddleware

from users.admin import CustomerAdmin
from users.customer_forms import CustomerChangeForm, CustomerCreationForm
from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from users.models import CustomerProfile, User


class ProfileAdminTesting(TestCase):
    """Testing the ProfileAdmin."""

    def create_request(self):
        """Creates request with "superuser" user."""
        factory = RequestFactory()
        req = getattr(factory, 'get')('/')
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.user = get_user_model().objects.create_superuser(
            email="testSuperuser@testemail.com",
            password="testpassword123",
        )
        return req

    def setUp(self):
        """Set up customer profile for testing."""
        User = get_user_model()
        user = User.objects.create_user(
            email='testUser@email.com',
            password='testpassword123',
        )
        self.customer = CustomerProfile.objects.create(
            user=user,
            first_name='Mohamed',
            last_name='Ayman',
            mobile_number='0111111111',
            address='11th St.',
            country='Egypt',
            date_of_birth=datetime.date(2000, 1, 1),
        )
        self.req = self.create_request()
        self.admin = CustomerAdmin(CustomerProfile, admin_site=admin.site)

    def test_list_display(self):
        """Test the admin list display."""
        list_display = self.admin.get_list_display_links(
            self.req,
            self.admin.list_display
        )
        self.assertEqual(list_display, ['get_user'])

    def test_forms(self):
        """Test that forms are set correctly."""
        self.admin.get_form(self.req)
        self.assertEqual(self.admin.form, CustomerCreationForm)
        self.admin.get_form(self.req, self.customer)
        self.assertEqual(self.admin.form, CustomerChangeForm)

    def test_save(self):
        """Test that the method saves the profile and its user."""
        customer = self.admin.get_queryset(self.req).first()
        customer_user = self.admin.get_queryset(self.req).first().user
        self.assertEqual(customer, self.customer)
        self.assertEqual(customer_user, self.customer.user)

    def test_delete(self):
        """Test that the method deletes the profile and its user."""
        self.admin.delete_model(self.req, self.customer)
        self.assertFalse(CustomerProfile.objects.filter(
            id=self.customer.id).exists())
        self.assertFalse(User.objects.filter(
            id=self.customer.user.id).exists())

    def test_delete_queryset(self):
        """Test that the method deletes the profiles and its users."""
        queryset = self.admin.get_queryset(self.req)
        self.admin.delete_queryset(self.req, queryset)
        self.assertFalse(CustomerProfile.objects.filter(
            id=self.customer.id).exists())
        self.assertFalse(User.objects.filter(
            id=self.customer.user.id).exists())
