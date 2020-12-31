"""Orders app models."""
from django.db import models
from django.shortcuts import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from .static import ORDER_STATUS, PRODUCT_PAYMENT_STATUS


def tracking_code_save(obj):
    """
     A function to generate a 10 character tracking_code
     and, see if it has been used.
    """
    if not obj.tracking_code:  # if there isn't a tracking_code
        obj.tracking_code = get_random_string(10)  # create one
        tracking_code_is_wrong = True
        while tracking_code_is_wrong:  # keep checking until we have a valid tracking_code
            tracking_code_is_wrong = False
            other_objs_with_tracking_code = type(obj).objects.filter(
                tracking_code=obj.tracking_code)
            if len(other_objs_with_tracking_code) > 0:
                # if any other objects have current tracking_code
                tracking_code_is_wrong = True
            if tracking_code_is_wrong:
                # create another tracking_code and check it again
                obj.tracking_code = get_random_string(10)


class Order(models.Model):
    """Order Model."""
    customer = models.ForeignKey(
        "users.CustomerProfile",
        verbose_name=_("customer"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    total_price = models.FloatField(_("total price"))
    paltform_fees_percentage = models.IntegerField(
        _("platform commission"), default=10)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    tracking_code = models.SlugField(
        _("tracking code"), max_length=10, blank=True)
    charge_code = models.CharField(
        _("charge code"), max_length=27, blank=True)
    status = models.PositiveIntegerField(_("status"), choices=ORDER_STATUS)

    def save(self, *args, **kwargs):
        """ Add Slug creating/checking to save method. """
        tracking_code_save(self)
        super(Order, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("orders:order_detail", kwargs={"pk": self.pk})


class BillingDetails(models.Model):
    """Model container for order billing deetails."""
    country = models.CharField(_("country"), max_length=50)
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    address = models.TextField(_("address"))
    city = models.CharField(_("city"), max_length=50)
    postcode = models.IntegerField(_("post code"))
    email = models.EmailField(_("email"), max_length=254)
    phone = models.IntegerField(_("phone"))
    order_notes = models.TextField(_("order notes"), blank=True, null=True)
    order = models.OneToOneField(
        Order,
        verbose_name=_("order"),
        on_delete=models.CASCADE,
        related_name="billing_details")

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class OrderProduct(models.Model):
    """Product in Order model."""
    product = models.ForeignKey(
        "products.Product", verbose_name=_("product"),
        on_delete=models.CASCADE, blank=True, null=True,
        related_name="order_product")
    product_qty = models.IntegerField(_("product quantity"))
    purchase_price = models.FloatField(_("purchase price"))
    total_price = models.FloatField(_("total price"))
    payment_status = models.PositiveSmallIntegerField(
        _("payment status"), choices=PRODUCT_PAYMENT_STATUS, default=2)
    payment_error = models.CharField(
        _("payment error"), max_length=50, null=True, blank=True)
    order = models.ForeignKey(Order, verbose_name=_(
        "order"), on_delete=models.CASCADE, related_name="order_product")
