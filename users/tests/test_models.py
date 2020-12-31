"""Testing Models & Signals."""
import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from shop.settings import AUTH_USER_MODEL
from users.models import VendorProfile, CustomerProfile


class CustomUserModelTests(TestCase):
    """Tests for User Model."""

    def setUp(self):
        """Define set up for tests."""
        self.User = get_user_model()

    def test_AUTH_VENDOR_MODEL(self):
        """Test the project uses our custom user."""
        self.assertEqual(AUTH_USER_MODEL, 'users.User')

    def test_USERNAME_FIELD(self):
        """Test that email is used instead of username."""
        self.assertEqual(self.User.USERNAME_FIELD, 'email')

    def test_create_user(self):
        """Test the UserManager create_user."""
        user = self.User.objects.create_user(
            email="testUser@testemail.com",
            password="testpassword123",
        )
        self.assertEqual(user.email, 'testUser@testemail.com')
        self.assertTrue(user.check_password('testpassword123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test the UserManager create_superuser."""
        superuser = self.User.objects.create_superuser(
            email="testSuperuser@testemail.com",
            password="testpassword123",
        )
        self.assertEqual(superuser.email, 'testSuperuser@testemail.com')
        self.assertTrue(superuser.check_password('testpassword123'))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_string_represention(self):
        user = self.User.objects.create_user(
            email="testUser@testemail.com",
            password="testpassword123",
        )
        self.assertEqual(user.__str__(), 'testUser@testemail.com')


class VendorProfileTests(TestCase):
    """Tests VendorProfile model."""

    def setUp(self):
        """Set up vendor profile for testing."""
        User = get_user_model()
        user = User.objects.create_user(
            email='testUser@email.com',
            password='testpassword123',
        )
        self.vendor = VendorProfile.objects.create(
            user=user,
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

    def test_user_is_vendor(self):
        """
        Test the set_user_to_vendor signal,
        checking that user is_vendor attribute is True.
        """
        self.assertTrue(self.vendor.user.is_vendor)

    def test_vendor_methods(self):
        """Test methods in the abstract superclass UserProfile."""
        self.assertEqual(self.vendor.get_full_name(), 'Mohamed Ayman')
        self.assertEqual(self.vendor.get_short_name(), "Mohamed")
        self.assertEqual(self.vendor.__str__(), 'Mohamed')
        self.assertEqual(self.vendor.get_absolute_url(), reverse(
            'users:vendorprofile_detail', kwargs={'pk': str(self.vendor.pk)}))


class CustomerProfileTests(TestCase):
    """Tests CustomerProfile model."""

    def setUp(self):
        """Set up vendor profile for testing."""
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

    def test_user_is_customer(self):
        """
        Test the set_user_to_customer signal,
        checking that user is_customer attribute is True.
        """
        self.assertTrue(self.customer.user.is_customer)
