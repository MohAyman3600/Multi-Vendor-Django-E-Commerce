"""Products app URL configration."""
from django.urls import path

from .views import ProductCreateView, ProductUpdateView
from .views import ProductListView, ProductDetail, CategoryListView


app_name = 'products'

urlpatterns = [
    path('add/', ProductCreateView.as_view(), name='product_create'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('list/', ProductListView.as_view(), name='product_list'),
    path('category_detail/<int:pk>/',
         CategoryListView.as_view(), name='category_detail'),
]
