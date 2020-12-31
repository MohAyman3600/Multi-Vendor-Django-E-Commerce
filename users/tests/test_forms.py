"""
Testing Forms.
There is no need to test User forms as we are using Django built-in forms.
Both Vendor and Customer forms inherit from the same Profile base forms
without adding any custom behaviour, so we will test only Vendor forms.
"""
from django.test import TestCase

from users.models import VendorProfile
from users.vendor_forms import VendorCreationForm, VendorChangeForm
from .helpers import TestData


class TestVendorCreationForm(TestCase):
    """Test Vendor creation form."""

    data = TestData()

    def setUp(self):
        """
        Set up form data and form instance.
        VENDOR class variable to bind user saved while testing to it.
        """
        self.form = VendorCreationForm(data=self.data.get_vendor_data())
        self.VENDOR = None

    def tearDown(self):
        """Make sure to delete VENDOR after each test."""
        if self.VENDOR:
            self.VENDOR.delete()
            self.VENDOR = None

    def test_email_field(self):
        """Test the CustomUserEmailFormField class."""
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.clean_email(), 'testVendor@email.com')
        self.assertEqual(
            self.form.cleaned_data['email'], 'testVendor@email.com')
        self.VENDOR = self.form.save()
        error_form = VendorCreationForm(data=self.data.get_vendor_data())
        self.assertFalse(error_form.is_valid())
        error = eval(error_form.errors['email'].as_json())
        error = error[0]
        self.assertEqual(error['message'], error_form.email_error_messages)
        self.assertEqual(error['code'], 'email_taken')

    def test_form_save(self):
        """Test the ProfileBaseCreationForm save method."""
        self.assertTrue(self.form.is_valid())
        self.VENDOR = self.form.save()
        self.assertTrue(isinstance(self.VENDOR, VendorProfile))
        self.assertEqual(self.VENDOR.user.email, 'testVendor@email.com')
        self.assertTrue(self.VENDOR.user.check_password('testpassword123'))
        self.assertTrue(self.VENDOR.user.is_vendor)


class TestVendorChangeForm(TestCase):
    """Test Vendor change form."""

    data = TestData()

    def setUp(self):
        """
        Set up form data and form instance.
        VENDOR class variable to bind user saved while testing to it.
        """
        vendor_data = self.data.get_vendor_data()
        form = VendorCreationForm(data=vendor_data)
        form.is_valid()
        self.VENDOR = form.save()
        self.form = VendorChangeForm(
            instance=self.VENDOR, data=vendor_data)

    def tearDown(self):
        """Make sure to delete VENDOR after each test."""
        if self.VENDOR:
            self.VENDOR.delete()
            self.VENDOR = None

    def test_initial_fields(self):
        """Test that initial fields are correctly set."""
        self.assertEqual(
            self.form.fields['email'].initial, 'testVendor@email.com')
        self.assertEqual(
            self.form.fields['password'].initial, self.VENDOR.user.password)

    def test_email_field_clean(self):
        """Test the CustomUserEmailFormField class."""
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.clean_email(),
                         self.form.fields['email'].initial)

    def test_form_save(self):
        """Test the ProfileBaseCreationForm save method."""
        changed_data = self.data.get_vendor_data().copy()
        changed_data['email'] = 'changetTestUser@email.com'
        changed_data['first_name'] = 'Ahmed'
        changed_data['company_name'] = 'KTS'
        form = VendorChangeForm(instance=self.VENDOR, data=changed_data)
        self.assertTrue(form.is_valid())
        changed_VENDOR = form.save()
        self.assertEqual(
            changed_VENDOR.user.email, 'changetTestUser@email.com')
        self.assertEqual(changed_VENDOR.first_name, 'Ahmed')
        self.assertEqual(changed_VENDOR.company_name, 'KTS')
