"""Custom User Manager."""
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager model where email is the unique identifier for authentication instead of username."""

    use_in_migrations = True

    def create_user(self, email, first_name, last_name, mobile_number, password, **extra_fields):
        """Create and save user with given email and password."""
        fields_names = ["email", "first_name", "last_name", "mobile_number"]
        values = [email, first_name, last_name, mobile_number]
        field_value_map = dict(zip(fields_names, values))
        for field, value in field_value_map.items():
            if not value:
                raise ValueError(_(f"The {field} must be set!"))
        if not mobile_number:
            raise ValueError(_("Mobile number must be set!"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creaete and save superuser with email, password and correct defaults."""
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)
