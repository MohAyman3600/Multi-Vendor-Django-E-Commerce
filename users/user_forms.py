"""Custom User forms."""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Form for Creating custom user.

    Creating user without profile, used in the admin site.
    """

    class Meta:
        """Meta Info."""

        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """
    Form for Changing custom user data.

    Changing user without profile, used in the admin site.
    """

    class Meta:
        """Meta Info."""

        model = User
        fields = ('email', 'password', 'is_active', 'is_staff',
                  'is_superuser')


class CustomUserEmailFormField(forms.Form):
    """
    Custom user fields mixin.

    Defines user email field and it's clean method
    to include in profile forms.
    """

    email_error_messages = _('This email already has an account')

    email = forms.EmailField(label=_('Email'), required=True)

    def clean_email(self):
        """
        Clean user's email field.
        Checks if there is a user with same email.
        """
        email = self.cleaned_data.get('email')
        if email == self.fields['email'].initial:
            return email
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError(
                self.email_error_messages,
                code='email_taken',
            )
        return email
