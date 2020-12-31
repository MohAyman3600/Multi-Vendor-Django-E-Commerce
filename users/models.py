
"""Custom User Models."""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager
from .static import STRIPE_STATUS


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email as the unique identifier.
    """

    username = None
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(_("is active"), default=True)
    is_staff = models.BooleanField(_("is staff"), default=False)
    is_superuser = models.BooleanField(_("is superuser"), default=False)

    is_vendor = models.BooleanField(_("is vendor"), default=False)
    is_customer = models.BooleanField(_("is customer"), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        """Meta Info."""

        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """Use email as string representation."""
        return self.email


class UserProfile(models.Model):
    """UserProfile to be used as base for all profiles."""

    user = models.OneToOneField(
        User, verbose_name=_("Django Custom User"), on_delete=models.CASCADE,
        related_name="%(class)s")

    picture = models.ImageField(
        _("picture"), blank=True, null=True)

    class Meta:
        """Meta Info."""

        abstract = True

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def __str__(self):
        """Use email as string representation."""
        return self.user.email

    def get_absolute_url(self):
        """Return the URL of model detail page."""
        class_name = self.__class__.__name__.lower()
        return reverse(f"users:{class_name}_detail", kwargs={"pk": self.pk})


class VendorProfile(UserProfile):
    """Vendor model extending User model."""

    rating = models.DecimalField(
        _("rating"), max_digits=5, decimal_places=2, default=0)
    stripe_id = models.CharField(_("stripe id"), max_length=50, blank=True)
    stripe_status = models.PositiveSmallIntegerField(
        _("stripe_status"), choices=STRIPE_STATUS, null=True, default=3)

    class Meta:
        """Meta Info."""

        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')


class CustomerProfile(UserProfile):
    """Customer model extending user model."""
    first_name = models.CharField(
        _("first name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(
        _("last name"), max_length=50, null=True, blank=True)
    mobile_number = models.CharField(
        _("phone"), max_length=50, null=True, blank=True)
    address = models.TextField(_("address"), null=True, blank=True)
    country = models.CharField(
        _("country"), max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(
        _("date of birth"), blank=True, null=True)

    class Meta:
        """Meta Info."""

        verbose_name = _('customer')
        verbose_name_plural = _('customers')
