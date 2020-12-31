"""Users URL configration."""
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    SignUpView,
    CustomLoginView,
    CustomLogoutView,
    VendorDetail,
    CustomerDetail,
)
from .stripe_views import (
    StripeAuthorizeView,
    StripeAuthorizeCallBackView,
    StripeAccountStatusWebHook,
)

app_name = 'users'

urlpatterns = [
    path(r'signup/', SignUpView.as_view(), name='signup'),

    path('login/', CustomLoginView.as_view(), name='login'),

    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path(
        'password_reset/', auth_views.PasswordResetView.as_view(),
        name='password_reset'),

    path(
        'password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),

    path('vendor/<int:pk>/', VendorDetail.as_view(),
         name='vendorprofile_detail'),

    path(
        'customer/<int:pk>/', CustomerDetail.as_view(),
        name='customerprofile_detail'),

    path(
        'stripe/authorize/', StripeAuthorizeView.as_view(),
        name='stripe_authorize'),
    path(
        'stripe/authorize/callback/', StripeAuthorizeCallBackView.as_view(),
        name='stripe_callback'),
    path(
        'stripe/status/', StripeAccountStatusWebHook,
        name='stripe_status'),
]
