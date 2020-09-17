"""Custom User forms."""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import forms
from .models import User, Vendor


class CustomerSignUpForm(UserCreationForm):
    """User (customer) signup form."""

    model = User
    fields = ('email', 'first_name', 'last_name', 'mobile_number',
              'address', ' picture', 'date_of_birth')

    def save(self):
        """Override to activate is_customer field."""
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        return user


class VendorSignUpForm(UserCreationForm):
    """User(Vendor) signup form with extra vendor fields."""

    company_name = forms.CharField(label='Company Name')
    company_website = forms.URLField(
        label='Your Company Website', required=False)
    product_desc = forms.TextField(label="Describe your product")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'mobile_number',
                  'address', ' picture', 'date_of_birth')

    def save(self):
        """Override to activate is_vendor field, create vendor instance and assign it's fields."""
        user = super().save(commit=False)
        user.is_vendor = True
        user.save()
        vendor = Vendor.objects.create(user=user)
        vendor.company_name = self.cleaned_data.get('company_name')
        vendor.company_website = self.cleaned_data.get('company_website')
        vendor.product_desc = self.cleaned_data.get('product_desc')
        return user


class CustomerChangeForm(UserChangeForm):
    """Form for updating user (customer)."""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'mobile_number',
                  'address', ' picture', 'date_of_birth')


class VendorChangeForm(UserChangeForm):
    """User(Vendor) signup form with extra vendor fields."""

    company_name = forms.CharField(label='Company Name')
    company_website = forms.URLField(
        label='Your Company Website', required=False)
    product_desc = forms.TextField(label="Describe your product")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'mobile_number',
                  'address', ' picture', 'date_of_birth')

    def save(self):
        """Override to activate is_vendor field, create vendor instance and assign it's fields."""
        user = super().save(commit=False)
        user.is_vendor = True
        user.save()
        vendor = Vendor.objects.create(user=user)
        vendor.company_name = self.cleaned_data.get('company_name')
        vendor.company_website = self.cleaned_data.get('company_website')
        vendor.product_desc = self.cleaned_data.get('product_desc')
        return user
