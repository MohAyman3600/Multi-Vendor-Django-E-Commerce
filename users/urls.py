"""Users URL configration."""
from django.urls import path

from .views import SignUpView, CustomLoginView

urlpatterns = [
    path('signup/(?P<user_type>\d+)/$', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
