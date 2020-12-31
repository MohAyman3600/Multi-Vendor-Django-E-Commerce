"""Main Pages URL configrtions."""
from django.urls import path, re_path
from .views import HomePageView, ErrorPageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    re_path(r'error/(?P<error_name>.+?)/(?P<error_msg>.+?)/$',
            ErrorPageView.as_view(), name='error'),
]
