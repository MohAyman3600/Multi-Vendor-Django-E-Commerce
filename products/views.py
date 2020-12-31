"""Prodcut model views."""

from django.forms.models import modelformset_factory
from django.shortcuts import redirect
from django.views.generic import UpdateView, DetailView, ListView
from django.views.generic.edit import FormView
from utils.multiformsviews import MultiFormsView
from cart.forms import CartAddProductForm

from .models import Image, ImageAlbum, Product, Category
from .forms import PictureWidget, ProductForm, ReviewForm


class ProductCreateView(MultiFormsView):
    """View for creating the product along with it's album."""
    form_classes = {
        'product': ProductForm,
        'album': modelformset_factory(model=Image, fields=('image', 'default',), extra=4),
    }
    prefixes = {
        'product': 'product',
        'album': 'album',
    }
    success_urls = {
        'product': 'users:vendorprofile_detail',
        'album': 'home',
    }
    template_name = "products/product_create.html"

    def post(self, request, *args, **kwargs):
        """
        Returns the method for proccesing multiple (product and album) forms.
        """
        form_prefixes = self.get_prefix_from_request(request)
        return self._proccess_multiple_forms(form_prefixes)

    def forms_valid(self, valid_forms):
        """Saves product along with its vendor and album."""
        product_form = valid_forms.get('product')
        album_formset = valid_forms.get('album')
        album = ImageAlbum.objects.create()
        for form in album_formset.cleaned_data:
            if form:
                Image.objects.create(
                    name=form['image']._get_name(), image=form['image'], defualt=form['default'],album=album)
        product = product_form.save(commit=False)
        product.vendor = self.request.user.vendorprofile
        product.album = album
        product.save()
        return redirect('users:vendorprofile_detail',
                        pk=self.request.user.vendorprofile.id)


class ProductUpdateView(UpdateView):
    """View for updating product and optionally it's album."""
    model = Product
    fields = ('title', 'desc', 'category',
              'is_featured', 'price', 'qty')
    template_name = "products/product_update.html"
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """Add the album form to the context."""
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        album_images = [item for item in product.album.images.all()]
        album_form = modelformset_factory(
            model=Image,
            fields=('image','default',),
            widgets={'image': PictureWidget},
            extra=4,
            max_num=len(album_images)
        )
        context['album_form'] = album_form
        return context

    def form_valid(self, form):
        """Saves the product with the new added images if any."""
        product = self.get_object()
        for img in form.files.keys():
            product.album.images.filter(image=img).delete()
            Image.objects.create(
                name=form.files[img]._get_name(),
                image=form.files[img],
                default=form['default'],
                album=product.album
            )
        return super().form_valid(form)


class ProductDetail(FormView, DetailView):
    """View for displaying product detail page."""
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = 'product'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        """Add 'add to cart' form to the context."""
        context = super().get_context_data(**kwargs)
        context['cart_add_form'] = CartAddProductForm()
        return context

    def form_valid(self, form):
        """Saves the product review ad redirects success URL."""
        instance = form.save(commit=False)
        instance.product = self.get_object()
        instance.auth = self.request.user
        instance.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        """Set form success URL to the same product detail page."""
        next = self.request.POST.get('next')
        return next


class ProductListView(ListView):
    """View for listing all products."""
    model = Product
    template_name = "products/prodcut_list.html"

    def get_context_data(self, **kwargs):
        """Add all categories to the context."""
        context = super().get_context_data(**kwargs)
        context['CATEGORIES'] = Category.objects.all()
        context['cart_add_form'] = CartAddProductForm()
        return context


class CategoryListView(DetailView):
    """View for listing product by category."""
    model = Category
    template_name = "products/category_detail.html"
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        """Add all categories to the context."""
        context = super().get_context_data(**kwargs)
        context['cart_add_form'] = CartAddProductForm()
        return context
