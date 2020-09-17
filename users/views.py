"""Custom User Views."""
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from .forms import CustomerSignUpForm, VendorSignUpForm
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import User


class SignUpView(CreateView):
    """Sign up view for all users."""

    template_name = 'account/signup.html'
    success_url = reverse_lazy('login')

    def get_form(self, request, obj=None, **kwargs):
        """Override to select form based on user type."""
        user_type = request.kwargs['user_type']
        if user_type == 'vendor':
            kwargs['form'] = VendorSignUpForm
        else:
            kwargs['form'] = CustomerSignUpForm
        return super(SignUpView, self).get_form(request, obj, **kwargs)


class CustomLoginView(LoginView):
    """Create custom login view to customize the redirect url."""

    template_name = 'account/login.html'

    def form_valid(self, form):
        """Override to redirect vendors to vendor dashbord."""
        if self.request.user.is_vendor:
            auth_login(self.request, form.get_user())
            url = reverse_lazy('vendor_dashboard')
            return redirect(url)

        return super(CustomLoginView, self).form_valid(form)
