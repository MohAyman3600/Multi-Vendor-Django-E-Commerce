"""Vendor profile forms."""
from .models import VendorProfile
from .profile_forms import ProfileBaseCreationForm, ProfileBaseChangeForm


class VendorCreationForm(ProfileBaseCreationForm):
    """Form for creating user associated with the related vendor profile."""

    class Meta:
        """Meta Info, includes vendor profile fields."""

        model = VendorProfile
        fields = (
            'email',
            'password1',
            'password2',
            'picture',
        )


class VendorChangeForm(ProfileBaseChangeForm):
    """Form for changing the user data, and the related vendor profile."""

    class Meta:
        """Meta Info, includes vendor profile fields."""

        model = VendorProfile
        fields = (
            'email',
            'password',
        )
