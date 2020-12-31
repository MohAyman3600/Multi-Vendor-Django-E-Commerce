"""Admin models."""
from django.contrib import admin

from .models import Category, Image, ImageAlbum, Product, Review


class ImageInline(admin.TabularInline):
    """Inline for images to display in album."""
    model = Image


class ImageAdmin(admin.ModelAdmin):
    """Image form."""
    list_display = ('name', 'album', 'image', 'default', 'album')

    class Meta:
        model = Image
        fields = ('image', 'default', 'width', 'length', 'album')


class ImageAlbumAdmin(admin.ModelAdmin):
    """ImageAlbum form"""
    inlines = [ImageInline]

    class Meta:
        model = ImageAlbum
        fields = '_all_'


class CategoryAdmin(admin.ModelAdmin):
    """Category form."""
    list_display = ('name',)
    filter_horizontal = ('products',)

    class Meta:
        model = Category
        fields = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    """Review form."""
    class Meta:
        model = Review
        fields = ('product', 'review', 'author')


class ProductAdmin(admin.ModelAdmin):
    """Product form."""
    list_display = ('vendor', 'title', 'price',)
    filter_horizontal = ('category',)

    class Meta:
        model = Product
        fields = ('vendor', 'title', 'desc',
                  'category', 'album', 'price', 'qty')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ImageAlbum, ImageAlbumAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Review, ReviewAdmin)
