"""Custom User admin site models."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Vendor
from .forms import CustomerSignUpForm, VendorSignUpForm, CustomerChangeForm, VendorChangeForm


class CustomerAdmin(UserAdmin):
    form = CustomerChangeForm
    add_form = CustomerSignUpForm
    model = User
    list_display = ['email', 'first_name', 'is_customer']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_customer=True)


class VendorInline(admin.StackedInline):
    model = Vendor
    can_delete = False
    verbose_name_plural = 'Vednors'
    fk_name = 'user'


class VendorAdmin(UserAdmin):
    inlines = (VendorInline,)


admin.site.register(User, CustomerAdmin)
admin.site.register(Vendor, VendorAdmin)
