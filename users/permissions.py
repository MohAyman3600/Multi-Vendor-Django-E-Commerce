"""User custom permission mixins."""
from string import Template
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.urls import reverse


class BaseUserCheckMixin(object):
    """
    Base Class for integrating custom user permission mixins with CBVs.

    You should subclass this and override user_check method.
    """

    permission_denied_redirect = ''
    error_name = ''
    error_msg = ''

    def user_check(self, user):
        """Check if user has the permission, and returns boolean."""
        return True

    def check_failed(self):
        """Redirect user if check filed."""
        return redirect(self.permission_denied_redirect,
                        error_name=self.error_name, error_msg=self.error_msg)

    def dispatch(self, request, *args, **kwargs):
        """
        Ovrride View dispatch method to check for permission before
        dispatching the view.

        The dispatch is the first method called in the view.
        """
        if not self.user_check(user=request.user):
            return self.check_failed()
        return super(BaseUserCheckMixin, self).dispatch(request,
                                                        *args,
                                                        **kwargs
                                                        )


class UserTypeRquiredPermissionMixin(BaseUserCheckMixin):
    """Permission to allow specific user types to access the view."""

    user_type_required = []
    error_name = "User Denied"
    error_msg = "Your account type cannot access this page."

    def user_check(self, user):
        """Return True if user in user_type_required, False otherwise."""
        if isinstance(self.user_type_required, str):
            self.user_type_required = [self.user_type_required]
        for usertype in self.user_type_required:
            if getattr(user, 'is_'+usertype, False):
                return True
        return False


class VendorNotAllowedPermissionMixin(BaseUserCheckMixin):
    """Permission to allow specific user types to access the view."""

    error_name = "Vendor Denied"
    error_msg = Template('Your vendor account cannot access this page.'
                         ' <a class="text-primary" style="font-size: 1.75rem;"'
                         'href="$url" >Log Out </a> to continue.')

    def user_check(self, user):
        """Return True if user in user_type_required, False otherwise."""
        if not isinstance(user, AnonymousUser):
            if user.is_vendor:
                return False
        return True

    def check_failed(self):
        """
        Add logout url to error message.
        """
        self.error_msg = self.error_msg.safe_substitute(
            url=reverse("users:logout")
        )
        return super(VendorNotAllowedPermissionMixin, self).check_failed()


class AnonymousUserRquiredPermissionMixin(BaseUserCheckMixin):
    """Permission to allow specific user types to access the view."""

    error_name = "You are Logged In"
    error_msg = Template('You are already logged in, do you wand to '
                         '<a class="text-primary" style="font-size: 1.75rem;"'
                         'href="$url" >Log Out </a> ?')

    def user_check(self, user):
        """Return True if user in user_type_required, False otherwise."""
        if isinstance(user, AnonymousUser):
            return True
        return False

    def check_failed(self):
        """
        Add logout url to error message.
        """
        self.error_msg = self.error_msg.safe_substitute(
            url=reverse("users:logout")
        )
        return super(AnonymousUserRquiredPermissionMixin, self).check_failed()
