
"""Custom User Models."""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser):
    """Custom user model with email as the unique identifier."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    mobile_number = models.CharField(_("phone"), max_length=50)
    address = models.TextField(_("address"))
    picture = models.ImageField(
        _("picture"), blank=True, null=True)
    country = models.CharField(_("country"), max_length=50)
    date_of_birth = models.DateField(
        _("date of birth"), blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(_("is active"), default=True)
    is_staff = models.BooleanField(_("is staff"), default=False)

    is_vendor = models.BooleanField(_("is vendor"), default=False)
    is_customer = models.BooleanField(_("is customer"), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [first_name, last_name, mobile_number]

    class Meta:
        """Meta Info."""

        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        """Use email as string representation."""
        return self.email


class Vendor(models.Model):
    """Vendor model extending User model with one-to-one relationship."""

    user = models.OneToOneField(
        User, verbose_name=_("user"), on_delete=models.CASCADE)
    company_name = models.CharField(_("company name"), max_length=50)
    company_website = models.URLField(_("company website"), max_length=50)
    product_desc = models.TextField(_("product desc"))
    rating = models.DecimalField(
        _("rating"), max_digits=5, decimal_places=2, default=0)
    stripe_id = models.CharField(_("stripe id"), max_length=50, blank=True)
    stripe_access_token = models.CharField(
        _("stripe access token"), max_length=50, blank=True)

    class Meta:
        """Meta Info."""

        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')

    def __str__(self):
        """Use email as string representation."""
        return self.user.email
