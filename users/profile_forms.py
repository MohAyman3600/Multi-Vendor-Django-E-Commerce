"""Profile models base forms."""
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls.base import reverse

from .models import User
from .user_forms import CustomUserEmailFormField


class ProfileBaseCreationForm(UserCreationForm, CustomUserEmailFormField):
    """
    Base form for profile creation.

    Defines __init__ and save method to save profile
    and it's associated user.
    """

    def __init__(self, *args, **kwargs):
        """
        Call grandparent (ModelForm) __init__ method.

        This is done to avoid the UserCreationForm __init__
        method which contains specific behaviour for the User model.
        """
        super(UserCreationForm, self).__init__(*args, **kwargs)

    @transaction.atomic
    def save(self, commit=True):
        """
        Save user with it's profile.
        User's is_vendor or is_customer field
        gets activated through signals.
        """
        try:
            user = User.objects.get(email=self.cleaned_data.get('email'))
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=self.cleaned_data.get('email'),
                password=self.cleaned_data.get('password2')
            )
        profile = super(UserCreationForm, self).save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile


class ProfileBaseChangeForm(UserChangeForm, CustomUserEmailFormField):
    """
    Base form for profile change.

    Defines __init__ and save method to save profile
    and it's associated user.
    """

    def __init__(self, *args, **kwargs):
        """
        Call ModelForm __init__ method.

        This is done to avoid the UserChangeForm __init__
        method which contains specific behaviour for the User model.
        Get password reset link.
        Provide initial data for the email and password fields.
        """
        super(UserChangeForm, self).__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            reset_url = '/admin/users/user/' + \
                str(self.instance.user.id)+'/password/'
            password.help_text = password.help_text.format(reset_url)
        self.fields['password'].initial = self.instance.user.password
        self.fields['email'].initial = self.instance.user.email

    @ transaction.atomic
    def save(self, commit=True):
        """Assign user email and password, and saves profile."""
        profile = super(UserChangeForm, self).save(commit=False)
        profile.user.email = self.cleaned_data['email']
        if commit:
            profile.save()
        return profile
