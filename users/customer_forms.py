"""Vendor profile forms."""
from .models import CustomerProfile
from .profile_forms import ProfileBaseCreationForm, ProfileBaseChangeForm


class CustomerCreationForm(ProfileBaseCreationForm):
    """Form for creating user associated with the related customer profile."""

    class Meta:
        """Meta Info, includes customer profile fields."""

        model = CustomerProfile
        fields = (
            'email', 'first_name', 'last_name', 'password1', 'password2',
            'mobile_number', 'address', 'picture', 'country'
        )


class CustomerChangeForm(ProfileBaseChangeForm):
    """Form for changing the user data, and the related customer profile."""

    class Meta:
        """Meta Info, includes customer profile fields."""

        model = CustomerProfile
        fields = (
            'email', 'first_name', 'last_name', 'password', 'mobile_number',
            'address', 'picture', 'country'
        )
