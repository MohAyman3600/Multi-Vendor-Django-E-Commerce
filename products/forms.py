from django import forms
from django.utils.safestring import mark_safe
from string import Template


from .models import Product, ImageAlbum, Image, Category, Review


class PictureWidget(forms.widgets.FileInput):
    """
    FileInput widget for displaying current image and input to change it.
    """

    def render(self, name, value, attrs=None, **kwargs):
        """Renders the input field and image int HTML and returns them."""
        name = value
        input_html = super().render(name, value, attrs=None, **kwargs)
        html = Template(
            """<img style="width:100;height:100;" src="/$link"/>""")
        img_html = mark_safe(html.substitute(link=value))
        return f'{input_html}{img_html}'


class ImageForm(forms.ModelForm):
    """Image form."""
    image = forms.ImageField()

    class Meta:
        model = Image
        fields = ('image', 'default',)

    def save(self, commit=True):
        """Set image name as the uploaded file name and save the image."""
        instance = super(ImageForm, self).save(commit=False)
        instance.name = instance.image.split('/')[-1]
        if commit:
            instance.save()
        return instance


class ImageAlbumForm(forms.ModelForm):
    """Form for image album."""
    class Meta:
        model = ImageAlbum
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    """Categroy Form."""
    class Meta:
        model = Category
        fields = ("name",)


class ReviewForm(forms.ModelForm):
    """Product review form."""
    class Meta:
        model = Review
        fields = ('review',)


class ProductForm(forms.ModelForm):
    """From for adding and changing products."""
    class Meta:
        model = Product
        exclude = ('album', 'vendor')
        fields = ('title', 'desc', 'category',
                  'is_featured', 'price', 'qty')


class ProductUpdateForm(forms.ModelForm):
    """From for adding and changing products"""
    class Meta:
        model = Product
        exclude = ('album', 'vendor')
        fields = ('title', 'desc', 'category',
                  'is_featured', 'price', 'qty')
