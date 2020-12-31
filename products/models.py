"""Products database models."""

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


def get_upload_path(instance, filename):
    """
    Creates image upload path dynamicly, depending on the uploading model.
    """
    model = instance.album.__class__._meta
    name = model.verbose_name_plural.replace(' ', '_')
    return f'static/{name}/images/{filename}'


class ImageAlbum(models.Model):
    """Model that contains multiple images."""

    def default(self):
        """Returns album default image."""
        image = self.images.filter(default=True).first()
        if image is None:
            image = self.images.first()
        return image

    def thumbnails(self):
        """Returns images in album with thumnail size."""
        return self.images.filter(width__lt=100, length__lt=100)

    class Meta:
        verbose_name = _("product_album")
        verbose_name_plural = _("product_album")


class Image(models.Model):
    """Image model to include in Product."""
    name = models.CharField(_("name"), default='image', max_length=50)
    image = models.ImageField(upload_to=get_upload_path)
    default = models.BooleanField(default=False)
    width = models.FloatField(default=100)
    length = models.FloatField(default=100)
    album = models.ForeignKey(
        ImageAlbum, related_name='images', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")


class Category(models.Model):
    """Products categories model."""
    name = models.CharField(_("Category"), max_length=50)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        """Retrun product string representation."""
        return self.name

    def get_absolute_url(self):
        """Return category URL."""
        return reverse("category_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    """Product Model."""
    vendor = models.ForeignKey(
        "users.VendorProfile", verbose_name=_("vendor"), null=True,
        default=None, on_delete=models.CASCADE, related_name='products')
    category = models.ManyToManyField(Category, verbose_name=_(
        "Categoty"), related_name='products')
    title = models.CharField(_("title"), max_length=50)
    desc = models.TextField(_("description"))
    album = models.OneToOneField(
        ImageAlbum, verbose_name=_("album"), on_delete=models.CASCADE)
    price = models.FloatField(_("price"))
    qty = models.IntegerField(_("quantity"))
    is_featured = models.BooleanField(_("featured"), default=False)
    add_date = models.DateTimeField(
        _("added"), auto_now_add=True, null=True)
    last_modified = models.DateTimeField(_("last modefied"), auto_now=True)

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        """Retrun product string representation."""
        return self.title

    def get_absolute_url(self):
        """Return product URL."""
        return reverse("products:product_detail", kwargs={"pk": self.pk})


class Review(models.Model):
    """Model for product reviews."""
    product = models.ForeignKey(
        Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='reviews')
    review = models.CharField(_("Review"), max_length=255)
    auth = models.ForeignKey(
        get_user_model(), verbose_name=_("Author"), on_delete=models.CASCADE)
